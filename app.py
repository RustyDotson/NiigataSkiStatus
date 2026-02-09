from flask import Flask, render_template
import os
import requests
import openmeteo_request
import sqlite3
import json
from config import DB_PATH, DESC_PATH, TIME_PATH

app = Flask(__name__)

@app.route('/')
def home():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT * FROM weather')
    weather_table = cur.fetchall()
    con.close()

    with open(DESC_PATH) as file:
        weather_codes = json.load(file)

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