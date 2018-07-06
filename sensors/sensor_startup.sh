#!/bin/bash

# add to raspberry pi start up folder or crontab
# check this out for more info: https://stackoverflow.com/questions/12973777/how-to-run-a-shell-script-at-startup
python /home/sensors/read_sensor.py & # must update the path
sleep 1
python /home/sensors/moisture_sensor.py & # must update the path