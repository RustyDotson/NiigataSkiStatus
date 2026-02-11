from db import get_db_connection

resorts = [["tainai", 38.02, 139.5, 73, 0, -4, 0, 3, 15, 281,],
           ["naeba", 36.8, 138.75, 75, -9, -13, 0, 10, 21, 316],
           ["mikawa", 37.72, 139.37, 73, 0, -5, 0, 1, 14, 289],
           ["ninox", 37.93, 139.44, 73, 0, -4, 0, 2, 18, 286],
           ["yuzawa kogen", 36.935, 138.785, 74, -8, -12, 0, 8, 20, 312],
           ["gala", 36.950932, 138.781754, 74, -7, -11, 0, 7, 19, 310],
           ["kagura", 36.860541, 138.725295, 73, -2, -8, 0, 5, 17, 292]]

# Insert into Postgres
with get_db_connection() as pg_con:
    with pg_con.cursor() as pg_cur:

        pg_cur.execute("""
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
        """)

        for resort in resorts:
            print(len(resort), resort)
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
                resort
            )

print("Migration complete")