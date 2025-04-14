

import os
import sys
import grpc
import replication
from concurrent import futures

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import protobuf generated files
from aggregator import aggregator_pb2
from aggregator import aggregator_pb2_grpc
from aggregator import checkpoint
from aggregator import logger

class AggregatorServicer(aggregator_pb2_grpc.AggregatorServicer):
    def __init__(self):
        self.num_shards = 3
        self.store = checkpoint.load_checkpoint()  # Load store from last snapshot

        # Replay WAL after checkpoint
        for entry in logger.load_log():
            key, value = entry['key'], entry['value']
            if key in self.store:
                self.store[key] += value
            else:
                self.store[key] = value

        self.update_count = 0  # To decide when to checkpoint

    def get_shard_id(self, key):
        return hash(key) % self.num_shards

    def Add(self, request, context):
        key, value = request.key, request.value
        logger.log_update(key, value)
        
        shard_id = self.get_shard_id(key)
        replication.write_to_shard(shard_id, key, value)
        
        if key in self.store:
            self.store[key] += value
        else:
            self.store[key] = value

        self.update_count += 1
        if self.update_count >= 5:  # Every 5 updates, save checkpoint
            checkpoint.save_checkpoint(self.store)
            self.update_count = 0

        return aggregator_pb2.AddResponse(status="success")

    def GetTotal(self, request, context):
        key = request.key
        shard_id = self.get_shard_id(key)
        value = replication.read_from_shard(shard_id, key)
        print(f"Queried {key} from shard {shard_id} = {value}")
        return aggregator_pb2.GetResponse(total=value)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aggregator_pb2_grpc.add_AggregatorServicer_to_server(AggregatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("✅ Server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()