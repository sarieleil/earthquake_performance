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
