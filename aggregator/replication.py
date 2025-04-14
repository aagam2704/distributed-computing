import database
import os

# Initialize database connections for each shard
shard_dbs = {
    0: database.LocalDB("shard_0.db"),
    1: database.LocalDB("shard_1.db"), 
    2: database.LocalDB("shard_2.db")
}

def write_to_shard(shard_id, key, value):
    """Write a key-value pair to the specified shard"""
    if shard_id not in shard_dbs:
        raise ValueError(f"Invalid shard_id: {shard_id}")
    shard_dbs[shard_id].update(key, value)

def read_from_shard(shard_id, key):
    """Read a value from the specified shard"""
    if shard_id not in shard_dbs:
        raise ValueError(f"Invalid shard_id: {shard_id}")
    return shard_dbs[shard_id].query(key)
