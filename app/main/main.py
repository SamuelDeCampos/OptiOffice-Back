from .model.user import UserModel
import time
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    user = UserModel.getUserById('9aaa9de6-bb0b-11eb-8529-0242ac130003')
    return user


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
