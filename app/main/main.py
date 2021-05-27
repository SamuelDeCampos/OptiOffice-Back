from .model.user import UserModel
import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
