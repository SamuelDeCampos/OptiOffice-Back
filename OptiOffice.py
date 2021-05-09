import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"
@app.route('/time')
def get_current_time():
    return {'time': time.time()}