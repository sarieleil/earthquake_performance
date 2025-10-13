# models.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "earthquakes.db")

def ensure_db_and_table():
    """Ensure the SQLite database and table exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Table columns match the normalized CSV columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place TEXT,
            mag REAL,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_earthquake(place, mag, time):
    """Insert a single earthquake record into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO earthquakes (place, mag, time) VALUES (?, ?, ?)",
        (place, mag, time)
    )
    conn.commit()
    conn.close()
