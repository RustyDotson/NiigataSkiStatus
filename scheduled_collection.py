import openmeteo_request
#import schedule
import time

def request_weather_info():
    print(time.ctime() + "updating database now.")
    openmeteo_request.update_db()
    print(time.ctime() + "Database Updated.")
    return ()


#schedule.every().day.at('06:00').do(request_weather_info)
#schedule.every(60).seconds.do(request_weather_info)
#schedule.every(5).seconds.do(request_weather_info)


#while True:
#    schedule.run_pending()
#    time.sleep(1)

if __name__ == "__main__":
    request_weather_info()