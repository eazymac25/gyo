from datetime import datetime
from time import sleep

import requests
import Adafruit_DHT as dht # easy package to deal with reading GPIO

SENSOR = dht.DHT11
SLEEP_TIME = 5*60 # let's post the temperature and humidity every 10 minutes
# works out to be 144 post requests every 12 hrs... I think we can live with that

url = 'http://eazymac25.pythonanywhere.com/rest/api/1/record'
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
}

def poll_sensor(pin=4):

    while True:

        current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        humidity, temp = dht.read_retry(SENSOR, pin)

        data = {
            "humidity": humidity,
            "temperature": temp,
            "ts": current_time
        }

        requests.post(
            url=url,
            data=data,
            headers=headers
        )

        sleep(SLEEP_TIME)