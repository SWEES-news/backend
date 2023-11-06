"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random

BIG_NUM = 100000000000000000000
MAX_EMAIL_LEN = 320
NAME = 'username'
MOCK_NAME = 'test'
PASSWORD = 'password'
MOCK_PASSWORD = '2'
EMAIL = 'email'
MOCK_EMAIL = '1@gmail.com'
EMAIL_TAIL = '@gmail.com'
EMAIL_TAIL_LEN = 10
MAX_MOCK_LEN = MAX_EMAIL_LEN - EMAIL_TAIL_LEN

# storage of users, email: tuple(username, password)
users = {
    MOCK_EMAIL: (MOCK_NAME, MOCK_PASSWORD)
}


# returns json of mock user
def get_mock_user():
    return {NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD, EMAIL: MOCK_EMAIL}


# gets a user with a random gmail address
def get_rand_user():
    rand_part = str(random.randint(0, BIG_NUM))
    if len(rand_part) > MAX_MOCK_LEN:
        rand_str = (rand_part[:MAX_MOCK_LEN])
    else:
        rand_str = rand_part
    rand_str += EMAIL_TAIL
    return {NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD, EMAIL: rand_str}


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}

# future use
# def init_app(app):
#     db.init_app(app)
#     Migrate(app, db)
#     return True
