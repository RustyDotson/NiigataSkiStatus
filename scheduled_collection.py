import openmeteo_request
#import schedule
import time
from config import *
import os

def request_weather_info():
    print("Trying to open DB at:", DB_PATH)
    print("Exists?", os.path.exists(DB_PATH))
    print("Dir exists?", os.path.exists(os.path.dirname(DB_PATH)))

    print("\n\n" + time.ctime() + ", updating database now.\n")
    openmeteo_request.update_db()
    print("\n" + time.ctime() + ", Database Updated.\n")
    return ()


#schedule.every().day.at('06:00').do(request_weather_info)
#schedule.every(60).seconds.do(request_weather_info)
#schedule.every(5).seconds.do(request_weather_info)


#while True:
#    schedule.run_pending()
#    time.sleep(1)

if __name__ == "__main__":
    request_weather_info()