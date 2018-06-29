"""
Simple flask app for logging temperature data from raspberry pi
"""
import re

from flask import Flask, jsonify, request
import mysql.connector as mysql

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'
