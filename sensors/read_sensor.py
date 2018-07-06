"""
read moisture
"""

from datetime import datetime
from time import sleep

import requests
import json
import Adafruit_DHT as dht # easy package to deal with reading GPIO

SENSOR = dht.DHT11
SLEEP_TIME = 2*60 # let's post the temperature and humidity every 2 minutes
# works out to be 360 post requests every 12 hrs... I think we can live with that

url = 'http://eazymac25.pythonanywhere.com/rest/api/1/record'
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
}

PIN = 4

def poll_sensor(pin=4):

    while True:

        current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        humidity, temp = dht.read_retry(SENSOR, pin)

        data = {
            "humidity": humidity,
            "temperature": temp,
            "ts": current_time
        }

        response = requests.post(
            url=url,
            data=json.dumps(data),
            headers=headers
        )

        sleep(SLEEP_TIME)

begin_poll = True
# retry_count = 10

# # on start up retry 10 times
# # if we can't get one success don't start polling
# for _ in range(retry_count):
#     try:
#         dht.read(SENSOR, PIN)
#         begin_poll = True
#         break
#     except:
#         begin_poll = False
#     sleep(.1)

# we want to be connected to the internet
status = requests.head(url='http://eazymac25.pythonanywhere.com/').status_code

while status != 200:
    status = requests.head(url='http://eazymac25.pythonanywhere.com/').status_code
    sleep(2)

if begin_poll and status==200:
    poll_sensor(pin=PIN)
