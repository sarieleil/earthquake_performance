<<<<<<< HEAD
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
=======
import pandas as pd

def load_csv_to_df(path):
    """Load CSV file into DataFrame and normalize column names."""
    df = pd.read_csv(path)
    # Normalize column names: lowercase, strip spaces
    df.columns = df.columns.str.strip().str.lower()
    return df

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km."""
    from math import radians, cos, sin, asin, sqrt
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c
>>>>>>> 4bcee31aebe365d7f23dc94f4d1db58e93222dd7
