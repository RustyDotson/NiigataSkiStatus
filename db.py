import os
import psycopg2

# DATABASE_URL should point to the Render database 
# (declared in cron job and environment variables to stay secure).
DATABASE_URL = os.environ.get("DATABASE_URL") 
print(DATABASE_URL)

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)