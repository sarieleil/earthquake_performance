from models import create_table, insert_earthquake

print("Starting test_db.py")

create_table()
insert_earthquake("San Francisco", 6.8, "2025-10-12 15:00:00")

print("Sample earthquake inserted successfully!")
