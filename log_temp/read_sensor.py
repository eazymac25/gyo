from datetime import datetime
from time import sleep

import Adafruit_DHT as dht # easy package to deal with reading GPIO

SENSOR = dht.DHT11

def poll_sensor(pin=4):

	while True:
		current_time = datetime.now()
		humidity, temp = dht.read_retry(sensor, pin)
		sleep(2.0)