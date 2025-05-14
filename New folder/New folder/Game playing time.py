import sqlite3
import time
from datetime import datetime

# --- Database Setup ---
def create_table():
    conn = sqlite3.connect('game_sessions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT,
            start_time TEXT,
            end_time TEXT,
            duration REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_session(game_name, start_time, end_time, duration):
    conn = sqlite3.connect('game_sessions.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO sessions (game_name, start_time, end_time, duration)
        VALUES (?, ?, ?, ?)
    ''', (game_name, start_time, end_time, duration))
    conn.commit()
    conn.close()

# --- Game Time Tracking ---
def play_game():
    game_name = input("Enter game name: ")
    input("Press Enter to START playing...")
    start = datetime.now()
    print(f"Started at {start.strftime('%Y-%m-%d %H:%M:%S')}")
    input("Press Enter to STOP playing...")
    end = datetime.now()
    print(f"Ended at {end.strftime('%Y-%m-%d %H:%M:%S')}")
    duration = (end - start).total_seconds() / 60  # duration in minutes
    print(f"Session Duration: {duration:.2f} minutes")
    save_session(game_name, start.isoformat(), end.isoformat(), duration)

# --- Main ---
if _name_ == "_main_":
    create_table()
    play_game()