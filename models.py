import pandas as pd
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///earthquakes.db")
engine = create_engine(DATABASE_URL)

def insert_earthquake_data(file):
    df = pd.read_csv(file)
    df.to_sql("earthquakes", engine, if_exists='replace', index=False)

def query_time_range(start, end):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, net, time, lat, lon FROM earthquakes WHERE time BETWEEN :start AND :end"),
            {"start": start, "end": end}
        )
        return [dict(row) for row in result]

def query_net_value(start_time, net, count):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, net, time, lat, lon 
                FROM earthquakes 
                WHERE net=:net AND time>=:start_time
                ORDER BY time ASC
                LIMIT :count
            """), {"net": net, "start_time": start_time, "count": count}
        )
        return [dict(row) for row in result]

def update_event(event_id, data):
    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE earthquakes
                SET time=:time, net=:net, lat=:lat, lon=:lon
                WHERE id=:id
            """), {**data, "id": event_id}
        )
