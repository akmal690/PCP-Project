import sqlite3
import time
import random
from datetime import datetime

# --- Database Setup ---
def create_table():
    conn = sqlite3.connect('typing_speed.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wpm REAL,
            accuracy REAL,
            duration REAL,
            test_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_result(wpm, accuracy, duration):
    conn = sqlite3.connect('typing_speed.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO results (wpm, accuracy, duration, test_date)
        VALUES (?, ?, ?, ?)
    ''', (wpm, accuracy, duration, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# --- Typing Speed Test Logic ---
sentences = [
    "Python is a programming language",
    "We love coding",
    "Typing speed test",
    "This is a sample sentence"
]

def typing_test():
    sentence = random.choice(sentences)
    print("Type this sentence:\n", sentence)
    input("Press Enter to start...")
    start = time.time()
    user_input = input()
    end = time.time()
    duration = end - start

    words = len(sentence.split())
    wpm = round((words / duration) * 60, 2)
    correct = sum(1 for a, b in zip(sentence.split(), user_input.split()) if a == b)
    accuracy = round((correct / words) * 100, 2)

    print(f"Time: {duration:.2f} seconds")
    print(f"Speed: {wpm} WPM")
    print(f"Accuracy: {accuracy}%")

    save_result(wpm, accuracy, duration)

# --- Main ---
if _name_ == "_main_":
    create_table()
    typing_test()