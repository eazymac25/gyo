
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/rest/api/1/record')
def create_record():
	pass

@app.route('/rest/api/1/records')
def create_records():
	pass

@app.route('/rest/api/1/record/<int:id>')
def get_record():
	pass

