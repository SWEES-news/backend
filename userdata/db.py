"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import userdata.db_connect as dbc

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
    dbc.connect_db()
    return dbc.fetch_all_as_dict(EMAIL, USER_COLLECT)


def add_user(email: str, username: str, password: int) -> str:
    if exists(email):
        raise ValueError(f'Duplicate Email: {email=}')
    if not email:
        raise ValueError('Email may not be blank')
    user = {}
    user[EMAIL] = email
    user[NAME] = username
    user[PASSWORD] = password
    dbc.connect_db()
    _id = dbc.insert_one(USER_COLLECT, user)
    return _id is not None


def del_user(email: str):
    if email in users:
        del users[email]
    if exists(email):
        dbc.del_one(USER_COLLECT, {EMAIL: email})
    else:
        raise ValueError(f'Delete failure: {email} not in database.')


def get_name(user):
    return user.get(NAME, '')


def exists(email: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {EMAIL: email})

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
