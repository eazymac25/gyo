
from flask import jsonify, request
import mysql.connector as mysql

from gyo_dash.app import app
from gyo_dash.config import sql_config

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

        result = {}
        cur.execute(insert, data)

        if cur.lastrowid:
            result = {"error": "", "lastrowid": cur.lastrowid}
        else:
            result = {"error": "Insert Error", "lastrowid": ""}

        conn.commit()
        # clean up and close all
        cur.close()
        conn.close()

        return jsonify(result)

    else:
        return jsonify({"error": "Incorrect Request Method - accept POST only", "lastrowid": ""})

@app.route('/rest/api/1/records', methods=['POST'])
def create_records():
    # TODO: implement me :)
    pass

@app.route('/rest/api/1/record/<int:record_id>', methods=['GET'])
def get_record(record_id):

    record = {}
    if request.method == 'GET':

        conn = mysql.connect(**sql_config)
        cur = conn.cursor(buffered=True)

        query = "SELECT * FROM sensor_data WHERE ID=%s" % record_id
        cur.execute(query)

        for ID, Humidity, Temperature, ts in cur:
            record = {
                "id": ID,
                "humidity": Humidity,
                "temperature": Temperature,
                "createTime": ts
            }
            break

        cur.close()
        conn.close()

        return jsonify({"error": "", "record": record})
    else:
        return jsonify({"error": "Only accept get request", "record": record})

@app.route('/rest/api/1/measureHistory', methods=['GET'])
def get_measurement_history():
    """
    We need an object that can hold size of time period and the window size:
    So 1W would be 1 Week and 1D would be 1 Day. 30 Minutes

    M - Minutes
    H - Hours
    D - Day
    W - Weeks

    Request Params: ?timeframe=30&period=M&startAt=0&maxResults=100
        tf (int): the time frame size eg 30
        period (str): enum M,H,D,W - the timeframe peirod
        startAt (int) OPTIONAL: id to start at - defaults to 0
        maxResults (int) OPTIONAL: total results to return - default to 100
    """
    measure_history = {}

    p_map = {
        'M': 'MINUTE',
        'H': 'HOUR',
        'D': 'DAY',
        'W': 'WEEK',
    }

    if request.method == 'GET':

        conn = mysql.connect(**sql_config)
        cur = conn.cursor()

        tf = int(request.args.get('timeframe', type=int))
        period = p_map[request.args.get('period', type=str)]
        start_at = int(request.args.get('startAt', default=0, type=int))
        max_results = int(request.args.get('maxResults', default=100, type=int))

        if start_at < 0 or max_results < 0:
            raise ValueError('startAt and maxResults must be greater than 0')

        measure_history = {
            "startAt": start_at,
            "max_results": max_results,
            "truncated": False,
            "records": []
        }
        OFFSET = 1 # this is to offset the limit to see if any more records exist
        query = """
            SELECT *
            FROM sensor_data
            WHERE ts >= NOW() - INTERVAL {0} {1}
            ORDER BY ts ASC
            LIMIT {2}, {3};
        """.format(tf, period, start_at, max_results+OFFSET)

        cur.execute(query)
        i = start_at + 1
        for pid, humidity, temperature, created in cur:

            if i > start_at + max_results:
                measure_history['truncated'] = True
            else: # i >= start_at and i <= start_at + max_results
                measure_history['records'].append(
                    {
                        "id": pid,
                        "humidity": humidity,
                        "temperature": temperature,
                        "createTime": created
                    })
            i += 1

        cur.close()
        conn.close()
        return jsonify({"errror": "", "measureHistory": measure_history})

    else:
        return jsonify({"error": "Only accept get request", "measureHistory": measure_history})
