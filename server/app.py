"""
Simple flask app for logging temperature data from raspberry pi
"""

from flask import Flask, jsonify, request
import mysql.connector as mysql

sql_config = {
    'host': 'eazymac25.mysql.pythonanywhere-services.com',
    # 'port': 3306, # should not needs this
    'database': 'eazymac25$gyo_logs',
    'user': 'eazymac25',
    'password': 'pypass2544',
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True,
}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/rest/api/1/record', methods=['POST'])
def create_record():
    """
    Basic creation of a single record
    request should be in the form:
        {
            "humidity": 48.0,
            "temperature": 23.0,
            "ts": "2018-02-09 06:10:22"
        }
    """
    if request.method == 'POST':
        req_data = request.get_json()
        conn = mysql.connect(**sql_config)
        cur = conn.cursor()

        insert = "INSERT INTO sensor_data (Humidity, Temperature, ts) VALUES (%s, %s, %s)"
        # unpack the data
        data = (
        	req_data.get('humidity'),
        	req_data.get('temperature'),
        	req_data.get('ts'),
        )
        cur.execute(insert, data)

        cur.close()
        cnx.close()
    else:
        return jsonify({"error": "Incorrect Request Method - accept POST only"})

@app.route('/rest/api/1/records', methods=['POST'])
def create_records():
	# TODO: implement me :)
	pass

@app.route('/rest/api/1/record/<int:id>', methods=['GET'])
def get_record():
    pass

