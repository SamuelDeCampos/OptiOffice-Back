import bcrypt
from supabase_py.client import SupabaseQueryBuilder
from .model import Model

userColumns = {
    'id': '',
    'username': '',
    'password': ''
}


class User(Model):
    def __init__(self):
        super().__init__(userColumns, 'users')

    def createUser(self, username: str, email: str, password: str):
        password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = {'username': username, 'email': email, 'password': password}

        self.__create([user])

    def getUserById(self, uuid: str) -> SupabaseQueryBuilder:
        return self.__read('*', f'id.eq.{uuid}')

    def getUserByLogin(self, login: str) -> SupabaseQueryBuilder:
        return self.__read('*', f'username.eq.{login},email.eq.{login}')


UserModel = User()
