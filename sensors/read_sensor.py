"""
read moisture
"""

from datetime import datetime
from time import sleep
import logging

import requests
import json
import Adafruit_DHT as dht # easy package to deal with reading GPIO

logging.basicConfig(filename=r'/home/pi/sensor.logs',level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

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
        try:
            response = requests.post(
                url=url,
                data=json.dumps(data),
                headers=headers
            )
        except Exception as e:
            logging.debug('Error posting to API: %s', e)

        sleep(SLEEP_TIME)

begin_poll = True
retry_count = 10

# on start up retry 10 times
# if we can't get one success don't start polling
for _ in range(retry_count):
    try:
        dht.read(SENSOR, PIN)
        begin_poll = True
        logging.info('begin polling set to true')
        break
    except Exception as e:
        logging.debug('Error polling %s', e)
        begin_poll = False
    sleep(.1)

# we want to be connected to the internet

status = 500

logging.info('STATUS %s', status)

while status != 200:

    try:
        status = requests.head(url='http://eazymac25.pythonanywhere.com/').status_code
    except Exception as e:
        logging.error('error: %s', e)

    logging.info('STATUS %s', status)
    sleep(2)

if begin_poll and status==200:
    logging.info('BEGIN POLLING')
    poll_sensor(pin=PIN)
