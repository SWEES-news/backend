"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random

ID_LEN = 24
BIG_NUM = 100000000000000000000
MOCK_ID = '0' * ID_LEN
MAX_EMAIL_LEN = 320
NAME = 'Username'
MOCK_NAME = 'test'
PASSWORD = 'Password'
MOCK_PASSWORD = 2
EMAIL = 'Email'
MOCK_EMAIL = '1@gmail.com'
EMAIL_TAIL = '@gmail.com'
EMAIL_TAIL_LEN = 10
MAX_MOCK_LEN = MAX_EMAIL_LEN - EMAIL_TAIL_LEN

# storage of users, email: tuple(username, password)
users = {
    MOCK_EMAIL: {NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD}
}


# returns json of mock user
def get_test_user():
    return {NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD, EMAIL: MOCK_EMAIL}


# returns a randomly generated mock email
def _get_random_email():
    rand_part = str(random.randint(0, BIG_NUM))
    if len(rand_part) > MAX_MOCK_LEN:
        rand_str = (rand_part[:MAX_MOCK_LEN])
    else:
        rand_str = rand_part
    return rand_str + EMAIL_TAIL


# gets a user with a random gmail address
def get_rand_test_user():
    rand_part = _get_random_email()
    return {NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD, EMAIL: rand_part}


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users() -> dict:
    return users


def add_user(email: str, username: str, password: int) -> str:
    if email in users:
        raise ValueError(f'Duplicate Email: {email=}')
    if not email:
        raise ValueError('Email may not be blank')
    users[email] = {NAME: username, PASSWORD: password}
    return _gen_id()


def get_name(user):
    return user.get(NAME, '')


def exists(name: str) -> bool:
    return name in get_users()

# future use
# def init_app(app):
#     db.init_app(app)
#     Migrate(app, db)
#     return True
