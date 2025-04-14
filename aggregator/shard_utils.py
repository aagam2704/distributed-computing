#NUM_SHARDS = 2  # Adjust as needed

#def get_shard(key: str) -> int:
 #   return hash(key) % NUM_SHARDS
##
import hashlib

def get_shard_index(key, num_shards):
    hash_digest = hashlib.sha256(key.encode()).hexdigest()
    return int(hash_digest, 16) % num_shards
