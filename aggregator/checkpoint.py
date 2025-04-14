import pickle
import os

CHECKPOINT_FILE = "checkpoint.pkl"

def save_checkpoint(store):
    """Save the current store state to a checkpoint file"""
    with open(CHECKPOINT_FILE, 'wb') as f:
        pickle.dump(store, f)

def load_checkpoint():
    """Load the store state from checkpoint file if it exists"""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'rb') as f:
            return pickle.load(f)
    return {}  # Return empty dict if no checkpoint exists
