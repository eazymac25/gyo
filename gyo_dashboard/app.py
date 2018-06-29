"""
Simple flask app for logging temperature data from raspberry pi
"""

from flask import Flask, jsonify, request, url_for, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

# this is a circular import but unused
# it allows us to expose the sensor api into the main flask application
from flask.api import sensor_api