from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os
from PIL import Image
import io
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
from datetime import datetime

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database setup
def init_db():
    conn = sqlite3.connect('fraud_signatures.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comparisons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            original_image BLOB,
            test_image BLOB,
            score REAL,
            is_fraud BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_comparison(user_id, orig_blob, test_blob, score, is_fraud):
    conn = sqlite3.connect('fraud_signatures.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO comparisons (user_id, original_image, test_image, score, is_fraud)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, orig_blob, test_blob, score, is_fraud))
    conn.commit()
    conn.close()

# Image similarity comparison
def compare_images(image1_path, image2_path):
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    img1 = cv2.resize(img1, (300, 100))
    img2 = cv2.resize(img2, (300, 100))
    score, _ = ssim(img1, img2, full=True)
    return score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    file1 = request.files['original']
    file2 = request.files['test']
    user_id = request.form.get('user_id', 'anonymous')

    if not file1 or not file2:
        return "Please upload both files."

    path1 = os.path.join(app.config['UPLOAD_FOLDER'], 'original.png')
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], 'test.png')

    file1.save(path1)
    file2.save(path2)

    score = compare_images(path1, path2)
    is_fraud = score < 0.75  # You can adjust threshold

    # Save images as binary blobs
    with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
        orig_blob = f1.read()
        test_blob = f2.read()

    insert_comparison(user_id, orig_blob, test_blob, score, is_fraud)

    result = "Forgery Detected ❌" if is_fraud else "Match ✅"
    return render_template("result.html", score=round(score, 2), result=result)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('fraud_signatures.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, timestamp, score, is_fraud FROM comparisons ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", rows=rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
