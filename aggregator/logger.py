import json
import os

LOG_FILE = "wal.log"  # Write-Ahead Log file

def log_update(key, value):
    """Log an update operation to the WAL"""
    with open(LOG_FILE, 'a') as f:
        json.dump({'key': key, 'value': value}, f)
        f.write('\n')  # Newline for each entry

def load_log():
    """Load all entries from the WAL"""
    if not os.path.exists(LOG_FILE):
        return []
        
    entries = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            entries.append(json.loads(line))
    return entries

def clear_log():
    """Clear the WAL (after checkpointing)"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
