import os
import sys
import grpc

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import protobuf generated files
from aggregator import aggregator_pb2
from aggregator import aggregator_pb2_grpc


def run():
    # Connect to gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = aggregator_pb2_grpc.AggregatorStub(channel)

    # Send Add requests
    response1 = stub.Add(aggregator_pb2.AddRequest(key="apple", value=10))
    print("Add Response 1:", response1.status)

    response2 = stub.Add(aggregator_pb2.AddRequest(key="apple", value=5))
    print("Add Response 2:", response2.status)

    # Send GetTotal request
    response = stub.GetTotal(aggregator_pb2.GetRequest(key="apple"))
    print("Total for 'apple':", response.total)

if __name__ == '__main__':
    run()