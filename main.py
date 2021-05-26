import time
from flask import Flask
from app.main.model.user import UserModel

app = Flask(__name__)

@app.route('/')
def hello():
    return UserModel.getUserByLogin('user_test')

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)