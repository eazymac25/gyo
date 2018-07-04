
from time import sleep

import RPi.GPIO as GPIO
import smtplib


EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "yourusername@gmail.com"
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


GPIO.setmode(GPIO.BCM)
channel = 17
GPIO.setup(channel, GPIO.IN)


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, moisture_callback)

def update_database:
    pass

def send_email:
    pass

def moisture_callback(channel):
    if GPIO.input(channel):
        # when the moisture is low
        pass
    else:
        # when the moisture is high
        pass
    pass

while True:
    sleep(10*60) # only need to wake up every 10 minutes
