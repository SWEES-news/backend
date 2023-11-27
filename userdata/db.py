"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import os

import pymongo as pm
# import userdata.db_connect as dbc

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
USER_COLLECT = 'users'

# storage of users, email: tuple(username, password)
users = {
    MOCK_EMAIL: {NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD}
}

MONGO_ID = '_id'


def connect_db():
    """
    Uniform connection method for the database.
    Returns a mongo client object and sets a global client variable.
    """
    global client
    if client is None:
        print("Initializing MongoDB client.")
        cloud_env = os.environ.get("CLOUD_MONGO", LOCAL)
        if cloud_env == CLOUD:
            password = os.environ.get("GAME_MONGO_PW")
            if not password:
                raise ValueError('Set password for cloud Mongo usage.')
            conn_str = (f'mongodb+srv://gcallah:{password}'
                        '@cluster0.mongodb.net/?retryWrites=true&w=majority')
            client = pm.MongoClient(conn_str)
            print("Connected to Mongo in the cloud.")
        else:
            client = pm.MongoClient()
            print("Connected to Mongo locally.")
    return client


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


def get_user_by_id(user_id: str):
    """
    Fetches a user from the database by their ID.
    """
    global client
    db = client.your_database_name
    users_collection = db.users
    user = users_collection.find_one({'_id': user_id})
    return user
