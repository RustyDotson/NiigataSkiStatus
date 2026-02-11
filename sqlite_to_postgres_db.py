import sqlite3
import os
from db import get_db_connection

SQLITE_DB_PATH = "weather.db"

# Connect to SQLite
sqlite_con = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cur = sqlite_con.cursor()

# Fetch all data
sqlite_cur.execute("SELECT * FROM weather")
rows = sqlite_cur.fetchall()

print(f"Found {len(rows)} rows in SQLite")

# Insert into Postgres
with get_db_connection() as pg_con:
    with pg_con.cursor() as pg_cur:

        """pg_cur.execute(\"""
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                location TEXT UNIQUE NOT NULL,
                lat DOUBLE PRECISION NOT NULL,
                lon DOUBLE PRECISION NOT NULL,

                weather_code INTEGER,
                temperature_2m_max DOUBLE PRECISION,
                temperature_2m_min DOUBLE PRECISION,
                rain_sum DOUBLE PRECISION,
                snowfall_sum DOUBLE PRECISION,
                wind_speed_10m_max DOUBLE PRECISION,
                wind_direction_10m_dominant DOUBLE PRECISION,

                updated_at TIMESTAMP DEFAULT NOW()
            );
        \""")"""

        for row in rows:
            print(len(row), row)
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
                ON CONFLICT (location) DO NOTHING
                """,
                row[:-1]
            )

print("Migration complete")

sqlite_con.close()