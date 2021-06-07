import bcrypt
import uuid
import datetime
import jwt
from model import Model
from typing import Union

from ..config import SECRET_KEY

MINIMUM_PASSWORD_LENGTH = 6


class User(Model):
    def __init__(self):
        super().__init__('users')
        self.schema = [
            {
                'name': 'id',
                'default': lambda model: uuid.uuid4()
            },
            {
                'name': 'username',
            },
            {
                'name': 'email',
                'validator': lambda value, model: len(model.select(['*'], [('email', 'eq', value)])) == 0
            },
            {
                'name': 'password',
                'validator': lambda value, model: len(value) >= 6,
                'mapper': lambda value, model: bcrypt.hashpw(bytes(value, encoding='utf-8'), bcrypt.gensalt()).decode()
            }
        ]

    def __map_to_client_model(self, row):
        del row['password']
        return row

    def __encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e


UserModel = User()