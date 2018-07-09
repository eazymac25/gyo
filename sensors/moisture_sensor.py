"""
Simple script to run at raspberry pi start up which logs whether the moisture
level is low or high

This will drive two things:
1) an updat to the GYO UI
2) An email notification from the server
"""

# TODO: Add error handling for if this script is run
# without the sensor connected to the specified pin/channel

from datetime import datetime
from time import sleep
import json
import logging

import RPi.GPIO as GPIO
import requests

logging.basicConfig(filename=r'/home/pi/moisture.logs',level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

url = 'http://eazymac25.pythonanywhere.com/rest/api/1/moisture'
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
}

CHANNEL = 26

status = 500

logging.info('STATUS %s', status)

while status != 200:

    try:
        status = requests.head(url='http://eazymac25.pythonanywhere.com/').status_code
    except Exception as e:
        logging.error('error: %s', e)

    logging.info('STATUS %s', status)
    sleep(2)

try:
    OLD_LEVEL = requests.get(url=url).json().get('record', {}).get('moistureLevel', None)
except Exception as e:
    OLD_LEVEL = None
    logging.debug('error checking last level %s', e)

def post_moisture(moisture_level):
    global OLD_LEVEL
    response = None

    if moisture_level != OLD_LEVEL:
        current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        data = {
            "moistureLevel": moisture_level,
            "createTime": current_time
        }

        try:
            response = requests.post(
                url=url,
                data=json.dumps(data),
                headers=headers
            )
            OLD_LEVEL = moisture_level
        except Exception as e:
            logging.debug('error posting data: %s', e)
            
    return response

def moisture_callback(channel):
    if GPIO.input(channel):
        # when the moisture is high
        post_moisture('LOW')
    else:
        # when the moisture is low
        post_moisture('HIGH')
    pass

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL, GPIO.IN)


GPIO.add_event_detect(CHANNEL, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(CHANNEL, moisture_callback)

while True:
    sleep(1) # we want to keep this running to register callbacks
