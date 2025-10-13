import pandas as pd
import sqlite3

# Read earthquake CSV file (make sure your file is in the same folder)
csv_file = "earthquakes.csv"  # <-- change if your file has another name
df = pd.read_csv(csv_file)

# Create SQLite database
conn = sqlite3.connect("earthquakes.db")
df.to_sql("earthquakes", conn, if_exists="replace", index=False)
conn.close()

print("✅ Database created successfully: earthquakes.db")
