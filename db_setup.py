import os
import csv
from models import init_db

# CSV file path (Render environment)
CSV_FILE = os.environ.get("CSV_FILE_PATH", "uploads/earthquakes.csv")

# Create uploads folder if not exists
os.makedirs("uploads", exist_ok=True)

if os.path.exists(CSV_FILE):
    print(f"Loading data from {CSV_FILE}...")
    init_db(CSV_FILE)
    print("Database initialized and CSV loaded successfully!")
else:
    print("No CSV found. Database created empty.")
    init_db()
