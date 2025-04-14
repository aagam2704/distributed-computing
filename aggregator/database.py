import sqlite3
import threading

class LocalDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value INTEGER)")

    def update(self, key, value):
        with self.lock:
            cur = self.conn.execute("SELECT value FROM kv WHERE key = ?", (key,))
            row = cur.fetchone()
            new_val = (row[0] if row else 0) + value
            self.conn.execute("INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)", (key, new_val))
            self.conn.commit()

    def query(self, key):
        with self.lock:
            cur = self.conn.execute("SELECT value FROM kv WHERE key = ?", (key,))
            row = cur.fetchone()
            return row[0] if row else 0
