"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import userdata.db_connect as dbc  # userdata.

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


# returns json of mock user
def get_test_user():
    return {NAME: MOCK_NAME, EMAIL: MOCK_EMAIL, PASSWORD: MOCK_PASSWORD}


# returns a randomly generated mock email
def _get_random_name():
    return str(random.randint(0, BIG_NUM))


# gets a user with a random gmail address
def get_rand_test_user():
    rand_part = _get_random_name()
    return {NAME: rand_part, EMAIL: MOCK_EMAIL, PASSWORD: MOCK_PASSWORD}


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, USER_COLLECT)


def add_user(username: str, email: str, password: str) -> str:
    if exists(username):
        raise ValueError(f'Duplicate Username: {username=}')
    if not username:
        raise ValueError('username may not be blank')
    user = {}
    user[NAME] = username
    user[EMAIL] = email
    user[PASSWORD] = password
    dbc.connect_db()
    _id = dbc.insert_one(USER_COLLECT, user)
    return str(_id) if _id else "False"


def verify_user(username: str, password: str) -> bool:
    dbc.connect_db()
    # Retrieve user from database using the fetch_one function
    user = dbc.fetch_one(USER_COLLECT, {NAME: username})
    if user and password == user[PASSWORD]:
        return True
    return False


def del_user(username: str):
    if exists(username):
        dbc.del_one(USER_COLLECT, {NAME: username})
    else:
        raise ValueError(f'Delete failure: {username} not in database.')


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {NAME: name})


def get_user_by_email(email: str):
    """
    Fetches a user from the database by their name.
    """
    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {EMAIL: email})


def store_article_submission(article_link: str, submitter_id: str) -> str:
    """
    Store the submitted article for review.
    """
    # Connect to the database
    dbc.connect_db()

    # Create a new article submission record
    submission_record = {
        "article_link": article_link,
        "submitter_id": submitter_id,
        # Add any other relevant fields, such as submission timestamp
    }

    # Insert the record into the database and retrieve the submission ID
    submission_id = dbc.insert_one('articles', submission_record)

    return submission_id
