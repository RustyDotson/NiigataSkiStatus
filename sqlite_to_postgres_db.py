import sqlite3
import os
import psycopg2
from config import DB_PATH

SQLITE_DB_PATH = DB_PATH

# Get Render database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    exit(1)

# Connect to SQLite
print(f"Connecting to local SQLite database at {SQLITE_DB_PATH}...")
sqlite_con = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cur = sqlite_con.cursor()

# Fetch all data
sqlite_cur.execute("SELECT * FROM weather")
rows = sqlite_cur.fetchall()

print(f"Found {len(rows)} rows in SQLite")

# Connect to Render Postgres
print("Connecting to Render database...")
pg_con = psycopg2.connect(DATABASE_URL)
pg_cur = pg_con.cursor()

# Clear existing data
print("Clearing Render database...")
pg_cur.execute("DELETE FROM weather")
pg_con.commit()

# Insert into Render Postgres
print("Inserting data into Render database...")
for row in rows:
    print(f"Inserting: {row[0]}")
    try:
        pg_cur.execute(
            """
            INSERT INTO weather (
                location,
                lat,
                lon,
                weather_code,
                temperature_2m_max,
                temperature_2m_min,
                rain_sum,
                snowfall_sum,
                wind_speed_10m_max,
                wind_direction_10m_dominant
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            row[0:10]
        )
    except Exception as e:
        print(f"Error inserting row {row}: {e}")

pg_con.commit()
print("Migration complete! Render database now has your local data.")

sqlite_con.close()
pg_con.close()