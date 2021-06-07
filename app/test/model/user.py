import unittest
from app.main.model.user import UserModel


class UserModelTest(unittest.TestCase):
    user_keys = ['id', 'username', 'password', 'email', 'created_at', 'updated_at', 'last_connection_at']
    user_test = {
        'uuid': 'a81c599f-eb23-4cce-8a2f-dfa8e408c547',
        'username': 'BetaTester',
        'email': 'beta@tester.com'
    }
    user_test_to_create = {
        'username': 'BetaTester2',
        'email': 'beta2@tester.com',
        'invalid_password': 'aaa',
        'valid_password': 'aaaaaaa'
    }

    def test_select(self):
        users = UserModel.select(['*'], [('id', 'eq', self.user_test.get('uuid'))])
        print(users)
        user = users[0]

        for key in self.user_keys:
            self.assertEqual(user.has(key), True)
        self.assertEqual(user.get('id'), self.user_test.get('id'))
        self.assertEqual(user.get('email'), self.user_test.get('email'))
        self.assertEqual(user.get('username'), self.user_test.get('username'))

        users_by_email = UserModel.select(['*'], [('email', 'eq', self.user_test.get('email'))])
        users_by_username = UserModel.select(['*'], [('username', 'eq', self.user_test.get('username'))])

        for key in self.user_keys:
            self.assertEqual(users_by_email[0].has(key), True)
        self.assertEqual(users_by_email[0].get('id'), self.user_test.get('id'))
        self.assertEqual(users_by_email[0].get('email'), self.user_test.get('email'))
        self.assertEqual(users_by_email[0].get('username'), self.user_test.get('username'))

        for key in self.user_keys:
            self.assertEqual(users_by_username[0].has(key), True)
        self.assertEqual(users_by_email[0].get('id'), users_by_username[0].get('id'))
        self.assertEqual(users_by_email[0].get('email'), users_by_username[0].get('email'))
        self.assertEqual(users_by_email[0].get('username'), users_by_username[0].get('username'))

    def test_createUser(self):
        new_user_existing_email = UserModel.createUser(
            self.user_test.get('username'),
            self.user_test.get('email'),
            self.user_test_to_create.get('valid_password')
        )

        self.assertEqual(new_user_existing_email, None)

        new_user_invalid_pwd = UserModel.createUser(
            self.user_test_to_create.get('username'),
            self.user_test_to_create.get('email'),
            self.user_test_to_create.get('invalid_password')
        )

        self.assertEqual(new_user_invalid_pwd, None)

        new_user = UserModel.createUser(
            self.user_test_to_create.get('username'),
            self.user_test_to_create.get('email'),
            self.user_test_to_create.get('valid_password')
        )

        for key in self.user_keys:
            self.assertEqual(new_user.has(key), True)
        self.assertEqual(new_user.get('username'), self.user_test_to_create.get('username'))
        self.assertEqual(new_user.get('email'), self.user_test_to_create.get('username'))

        fetched_new_user = UserModel.getUserById(new_user.get('id'))

        for key in self.user_keys:
            self.assertEqual(fetched_new_user.has(key), True)
        for key, value in new_user:
            self.assertEqual(fetched_new_user.has(key), True)
            self.assertEqual(fetched_new_user.get(key), new_user.get(key))