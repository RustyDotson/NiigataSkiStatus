import openmeteo_requests
import requests_cache
import pandas as pd
import time
from retry_requests import retry
import json
import math
from config import *

import sqlite3


def get_data(lat, long):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "rain_sum", "snowfall_sum", "wind_speed_10m_max", "wind_direction_10m_dominant"],
	    "timezone": "Asia/Tokyo",
	    "forecast_days": 1,
        "models": "jma_seamless"
    }
    
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(3).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(4).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(6).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    daily_dataframe = pd.DataFrame(data = daily_data)
    #print(daily_dataframe)
    return(daily_dataframe)


def create_weather_db(con, cur, locations):

    weather_table_exists = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather';")

    if weather_table_exists.fetchone() is None:
        cur.execute("CREATE TABLE weather(location, long, lat, weather_code, temperature_2m_max, temperature_2m_min, rain_sum, snowfall_sum, wind_speed_10m_max, wind_direction_10m_dominant)")
        for key in locations:
            cur.execute("INSERT INTO weather VALUES (\'" + key + "\', \'" + locations[key][0] + "\', \'" + locations[key][1] + "\', NULL, NULL, NULL, NULL, NULL, NULL, NULL)")
        
        con.commit()

        db_content = cur.execute("SELECT * FROM weather")
        db_content.fetchall()
        

        return
    

def update_db():

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur2 = con.cursor()
    weather_codes = open(DESC_PATH, 'r')


    for row in cur.execute("SELECT * FROM weather"):
        fetched_weather_data = get_data(row[1], row[2])
        cur2.execute("UPDATE weather SET weather_code = \'" +   str(math.floor(fetched_weather_data['weather_code'][0])) +
                     "\', temperature_2m_max = \'" +            str(math.floor(fetched_weather_data['temperature_2m_max'][0])) + 
                     "\', temperature_2m_min = \'" +            str(math.floor(fetched_weather_data['temperature_2m_min'][0])) + 
                     "\', rain_sum = \'" +                      str(math.floor(fetched_weather_data['rain_sum'][0])) + 
                     "\', snowfall_sum = \'" +                  str(math.floor(fetched_weather_data['snowfall_sum'][0])) + 
                     "\', wind_speed_10m_max = \'" +            str(math.floor(fetched_weather_data['wind_speed_10m_max'][0])) + 
                     "\', wind_direction_10m_dominant = \'" +   str(math.floor(fetched_weather_data['wind_direction_10m_dominant'][0])) + 
                     "\' WHERE location = \'" + row[0] + "\'")
    
    con.commit()
    store_update_time()
    return


def store_update_time():
    file = open(TIME_PATH, "w")
    file.write(time.ctime())
    file.close()


def test_function():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur2 = con.cursor()

    file = open(DESC_PATH)
    weather_data = json.load(file)

    print(weather_data['75']['day']['description'])
    

    for row in cur.execute("SELECT * FROM weather"):
        fetched_weather_data = get_data(row[1], row[2])
        cur2.execute("UPDATE weather SET weather_code = 'YAAAAAR', temperature_2m_max = \'" +            str(fetched_weather_data['temperature_2m_max'][0]) + 
                     "\', temperature_2m_min = \'" +            str(fetched_weather_data['temperature_2m_min'][0]) + 
                     "\', rain_sum = \'" +                      str(fetched_weather_data['rain_sum'][0]) + 
                     "\', snowfall_sum = \'" +                  str(fetched_weather_data['snowfall_sum'][0]) + 
                     "\', wind_speed_10m_max = \'" +            str(fetched_weather_data['wind_speed_10m_max'][0]) + 
                     "\', wind_direction_10m_dominant = \'" +   str(fetched_weather_data['wind_direction_10m_dominant'][0]) + 
                     "\' WHERE location = \'" + row[0] + "\'")
        con.commit()


if __name__ == "__main__":
    update_db()