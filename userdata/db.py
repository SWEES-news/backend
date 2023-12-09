"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import userdata.db_connect as dbc # userdata.
import bcrypt

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

# storage of users
users = {
    MOCK_EMAIL: {NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD}
}

MONGO_ID = '_id'


# returns json of mock user
def get_test_user():
    return {EMAIL: MOCK_EMAIL, NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD}


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
    return {EMAIL: rand_part, NAME: MOCK_NAME, PASSWORD: MOCK_PASSWORD}


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(EMAIL, USER_COLLECT)


def add_user(email: str, username: str, password: str) -> str:
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


def store_article_submission(article_link: str, submitter_id: str) -> str:
    """
    Store the submitted article for review.

    :param article_link: The URL of the article being submitted.
    :param submitter_id: The ID of the user submitting the article.
    :return: A unique ID for the article submission.
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
