from db import DATABASE_URL
import openmeteo_request
import time
from config import *

def request_weather_info():
    print("Trying to open DB at:", DATABASE_URL)

    print("\n\n" + time.ctime() + ", updating database now.\n")
    openmeteo_request.update_db()
    print("\n" + time.ctime() + ", Database Updated.\n")
    return ()


if __name__ == "__main__":
    request_weather_info()