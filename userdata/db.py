"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

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

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("GAME_MONGO_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://gcallah:{password}'
                                    + '@cluster0.eqxbbqd.mongodb.net/'
                                    + '?retryWrites=true&w=majority')
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()


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
