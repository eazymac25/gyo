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

import RPi.GPIO as GPIO
import requests

url = 'http://eazymac25.pythonanywhere.com/rest/api/1/moisture'
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
}

CHANNEL = 26

def post_moisture(moisture_level):

    current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

    data = {
        "moistureLevel": moisture_level,
        "createTime": createTime
    }

    response = requests.post(
        url=url,
        data=json.dumps(data),
        headers=headers
    )
    return response

def moisture_callback(channel):
    if GPIO.input(channel):
        # when the moisture is high
        post_moisture('HIGH')
    else:
        # when the moisture is low
        post_moisture('LOW')
    pass

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHANNEL, GPIO.IN)


GPIO.add_event_detect(CHANNEL, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(CHANNEL, moisture_callback)

while True:
    sleep(1) # we want to keep this running to register callbacks
