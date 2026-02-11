import os
import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg.connect(DATABASE_URL)