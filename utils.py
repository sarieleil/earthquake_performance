# utils.py
"""
Utility functions:
- load_csv_to_df: read CSV and normalize column names.
- haversine_km: compute distance (if needed later).
"""
import pandas as pd
import math
from typing import Tuple

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # lowercase all columns
    df.columns = [c.strip() for c in df.columns]
    lower_map = {c: c.lower() for c in df.columns}
    df = df.rename(columns=lower_map)

    # ensure standard names
    # candidate latitude names: 'latitude'
    # candidate longitude names: 'longitude'
    # magnitude: 'mag' or 'magnitude'
    # time: 'time'
    if 'mag' not in df.columns and 'magnitude' in df.columns:
        df = df.rename(columns={'magnitude': 'mag'})
    if 'mag' not in df.columns and 'magnitude' in df.columns:
        df = df.rename(columns={'Magnitude': 'mag'})

    # time usually 'time'
    # place maybe 'place'
    # net maybe 'net'
    return df

def load_csv_to_df(path: str) -> pd.DataFrame:
    """Load earthquake CSV, normalize column names, and ensure minimal columns exist."""
    df = pd.read_csv(path)
    df = normalize_columns(df)

    # ensure expected columns exist (add empty columns if missing)
    for col in ('place', 'mag', 'time', 'latitude', 'longitude', 'net'):
        if col not in df.columns:
            df[col] = pd.NA

    # convert mag to numeric where possible
    df['mag'] = pd.to_numeric(df['mag'], errors='coerce')
    return df

def haversine_km(lat1, lon1, lat2, lon2) -> float:
    # returns distance in kilometers
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))
