from flask import Flask, render_template
import os
import requests
import openmeteo_request
import sqlite3
import json

app = Flask(__name__)

@app.route('/')
def home():
    con = sqlite3.connect('weather.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM weather')

    file = open("descriptions.json")
    weather_codes = json.load(file)

    return render_template('home.html', test = cur, weather_code_info = weather_codes, update_time = open("update_time.txt").readline())

@app.route('/hellotwo')
def hello_world_two():
    return 'Hello Again!'