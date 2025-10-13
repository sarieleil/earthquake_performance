# models.py
<<<<<<< HEAD
"""
Database helper for SQLite operations.
Creates 'earthquakes' table and exposes query/modify functions.
"""
import sqlite3
import os
import json
from typing import List, Tuple, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "earthquakes.db")

def get_conn():
    # don't share connections across threads
    return sqlite3.connect(DB_PATH, isolation_level=None)

def ensure_db_and_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS earthquakes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place TEXT,
        mag REAL,
        time TEXT,
        latitude REAL,
        longitude REAL,
        net TEXT,
        raw_json TEXT
    )
    """)
    # indexes to speed queries
    cur.execute("CREATE INDEX IF NOT EXISTS idx_time ON earthquakes(time)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_net ON earthquakes(net)")
    conn.commit()
    conn.close()

def insert_earthquake(place, mag, time, latitude=None, longitude=None, net=None, raw_json=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO earthquakes (place, mag, time, latitude, longitude, net, raw_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (place, mag, time, latitude, longitude, net, json.dumps(raw_json) if raw_json else None)
    )
    conn.close()

def count_rows() -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM earthquakes")
    c = cur.fetchone()[0]
    conn.close()
    return c

def query_time_range(start_time: str, end_time: str) -> List[Tuple[Any,...]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, net, time, latitude, longitude, place, mag FROM earthquakes WHERE time BETWEEN ? AND ?", (start_time, end_time))
    rows = cur.fetchall()
    conn.close()
    return rows

def query_net_count(start_time: str, net_value: str, count: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, net, time, latitude, longitude, place, mag FROM earthquakes WHERE time >= ? AND net = ? ORDER BY time ASC LIMIT ?", (start_time, net_value, count))
    rows = cur.fetchall()
    conn.close()
    return rows

def modify_by_time(target_time: str, updates: dict) -> int:
    """
    Modify record(s) that exactly match target_time. updates is dict column->value.
    Returns number of rows updated.
    """
    allowed = {'place','mag','time','latitude','longitude','net'}
    items = [(k, updates[k]) for k in updates if k in allowed]
    if not items:
        return 0
    set_clause = ', '.join([f"{k} = ?" for k,_ in items])
    params = [v for _,v in items] + [target_time]
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE earthquakes SET {set_clause} WHERE time = ?", params)
    updated = cur.rowcount
    conn.commit()
    conn.close()
    return updated
=======
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
>>>>>>> 4bcee31aebe365d7f23dc94f4d1db58e93222dd7
