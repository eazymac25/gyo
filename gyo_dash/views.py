"""
Simple flask app for logging temperature data from raspberry pi
"""
from gyo_dash import app
from flask import request, url_for, render_template


@app.route('/')
def index():
    return render_template('base.html')
