from flask import Flask, render_template
import os
import requests
import openmeteo_request
import sqlite3
import json
from config import DB_PATH, DESC_PATH, TIME_PATH
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    #con = sqlite3.connect(DB_PATH)
    #con = get_db_connection()
    with get_db_connection() as con:
        with con.cursor() as cur:
            cur.execute('SELECT * FROM weather')
            weather_table = cur.fetchall()

    with open(DESC_PATH) as file:
        # descriptions.json keys are strings; convert to ints for easier lookup
        raw_codes = json.load(file)
        weather_codes = {int(k): v for k, v in raw_codes.items()}

    with open(TIME_PATH) as file:
        update_time = file.readline().strip()

    return render_template(
        "home.html", 
        weather = weather_table, 
        weather_code_info = weather_codes, 
        update_time = update_time
    )

@app.route('/hellotwo')
def hello_world_two():
    return 'Hello Again!'

if __name__ == '__main__':
    app.run(debug=True, port=5001)