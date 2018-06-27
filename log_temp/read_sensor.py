from datetime import datetime
from time import sleep

import Adafruit_DHT as dht # easy package to deal with reading GPIO

SENSOR = dht.DHT11

def poll_sensor(pin=4):

	while True:
		current_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
		humidity, temp = dht.read_retry(SENSOR, pin)
		sleep(2.0)