import sqlite3
import os

DB_PATH = 'database/signatures.db'
os.makedirs('database', exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS comparisons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original TEXT,
                        test TEXT,
                        similarity REAL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()

def save_result(original, test, similarity):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO comparisons (original, test, similarity) VALUES (?, ?, ?)",
                  (original, test, similarity))
        conn.commit()

init_db()
