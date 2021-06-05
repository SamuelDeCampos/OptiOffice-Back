import bcrypt
import uuid
from ..db_client import client
from typing import Union

MINIMUM_PASSWORD_LENGTH = 6


class User:
    def __init__(self):
        self.table = 'users'
        self.client_user = ['id', 'username', 'email', 'created_at']

    def __userAlreadyExists(self, email: str) -> bool:
        already_existing_user = client.select(self.table, ['*'], [('email', 'eq', email)])

        if len(already_existing_user) > 0:
            return True
        return False

    def __checkPasswordValidity(self, password: str) -> bool:
        return len(password) > MINIMUM_PASSWORD_LENGTH

    def __encryptPassword(self, password: str) -> str:
        return bcrypt.hashpw(bytes(password, encoding='utf-8'), bcrypt.gensalt()).decode()

    def getUserById(self, uuid: str) -> dict[str, object]:
        return client.select(self.table, self.client_user, [('id', 'eq', uuid)])

    def getUserByLogin(self, login: str) -> dict[str, object]:
        return client.select(self.table, self.client_user, [('username', 'eq', login, 'email', 'eq', login)])

    def createUser(self, username: str, email: str, password: str) -> Union[dict[str, object], None]:
        if self.__userAlreadyExists(email):
            return None
        if not self.__checkPasswordValidity(password):
            return None

        user = {
            'id': uuid.uuid4(),
            'username': username,
            'email': email,
            'password': self.__encryptPassword(password)
        }

        return client.insert(self.table, [user])

    def updateUsername(self, uuid: str, new_username: str) -> dict[str, object]:
        return client.update(self.table, {'username': new_username}, [('id', 'eq', uuid)])

    def updateEmail(self, uuid: str, new_email: str) -> Union[dict[str, object], None]:
        if self.__userAlreadyExists(new_email):
            return None
        return client.update(self.table, {'email': new_email}, [('id', 'eq', uuid)])

    def updatePassword(self, uuid: str, new_password: str) -> Union[dict[str, object], None]:
        if self.__checkPasswordValidity(new_password):
            return None

        password = self.__encryptPassword(new_password)

        return client.update(self.table, {'password': password}, [('id', 'eq', uuid)])

    def deleteUser(self, uuid: str) -> dict[str, object]:
        return client.delete(self.table, ['id', 'eq', uuid])


UserModel = User()
