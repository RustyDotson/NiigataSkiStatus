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

    file = open(DESC_PATH)
    weather_codes = json.load(file)

    return render_template("home.html", test = cur, weather_code_info = weather_codes, update_time = open(TIME_PATH).readline())

@app.route('/hellotwo')
def hello_world_two():
    return 'Hello Again!'