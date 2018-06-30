from flask import Flask

app = Flask(__name__)

import gyo_dash.views
from gyo_dash.api import sensor_api