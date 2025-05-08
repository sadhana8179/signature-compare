import sqlite3
from PIL import Image
import io

def create_database():
    conn = sqlite3.connect("fraud_signatures.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS signatures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        signature_image BLOB NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_fraud BOOLEAN DEFAULT 0,
        prediction_score REAL
    )
    """)
    conn.commit()
    conn.close()

def insert_signature(user_id, image_path, is_fraud=False, score=None):
    with open(image_path, "rb") as file:
        image_blob = file.read()
    conn = sqlite3.connect("fraud_signatures.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO signatures (user_id, signature_image, is_fraud, prediction_score)
    VALUES (?, ?, ?, ?)
    """, (user_id, image_blob, int(is_fraud), score))
    conn.commit()
    conn.close()

def fetch_fraud_signatures():
    conn = sqlite3.connect("fraud_signatures.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, timestamp, prediction_score FROM signatures WHERE is_fraud = 1")
    results = cursor.fetchall()
    conn.close()
    return results

def display_signature(signature_id):
    conn = sqlite3.connect("fraud_signatures.db")
    cursor = conn.cursor()
    cursor.execute("SELECT signature_image FROM signatures WHERE id = ?", (signature_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
        image = Image.open(io.BytesIO(data[0]))
        image.show()

# ----- Run the steps -----
print("✅ Running main.py")
create_database()
insert_signature("user123", "signature1.png.jpeg", is_fraud=True, score=0.95)
print("📄 Fraud Signatures:")
print(fetch_fraud_signatures())
print("🖼️ Displaying signature image...")
display_signature(1)

