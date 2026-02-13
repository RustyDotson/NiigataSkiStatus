"""
This is an early script used to migrate data from the local Sqlite3 database
to the Postgres database hosted on Render.com. Currently not in use, but may
be useful in the future.
""" 

import sqlite3
from db import get_db_connection

SQLITE_DB_PATH = "weather.db"

# Connect to SQLite db
sqlite_con = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cur = sqlite_con.cursor()

# Fetch all data from SQLite weather table
sqlite_cur.execute("SELECT * FROM weather")
rows = sqlite_cur.fetchall()

print(f"Found {len(rows)} rows in SQLite")

# Insert into Postgres
with get_db_connection() as pg_con:
    with pg_con.cursor() as pg_cur:
        # Create table if one doesnt exist. Currently not needed, but may be useful in the future.
        """
        pg_cur.execute(\"""
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
        \""")
        """

        # Iterates through each entry in the sqlite weather table 
        # and inserts into the Postgres weather table.

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