"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import userdata.db_connect as dbc  # userdata.
import bcrypt

# ------ configuration for MongoDB ------ #
USER_COLLECT = 'users'
ARTICLE_COLLECTION = 'articles'
# field name for user ID in the articles collection
USER_ID_FIELD = 'submitter_id'

# ------ DB fields ------ #
NAME = 'Username'
EMAIL = 'Email'
PASSWORD = 'Password'


# ------ DB rules ------ #
ID_LEN = 24
BIG_NUM = 100000000000000000000
MAX_EMAIL_LEN = 320
EMAIL_TAIL = '@gmail.com'
EMAIL_TAIL_LEN = 10


# ------ mock values ------ #
MOCK_ID = '0' * ID_LEN
MOCK_NAME = 'test'
MOCK_EMAIL = '1@gmail.com'
MOCK_PASSWORD = 'abcdef'
MOCK_NAME_2 = 'updated'
MOCK_EMAIL_2 = 'example@gmail.com'
MOCK_PASSWORD_2 = 'ghijkl'
MAX_MOCK_LEN = MAX_EMAIL_LEN - EMAIL_TAIL_LEN
# MOCK_USER_REMOVED = { "acknowledged" : True, "deletedCount" : 1 }


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


def update_test_user():
    return {NAME: MOCK_NAME_2, EMAIL: MOCK_EMAIL_2, PASSWORD: MOCK_PASSWORD_2}


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
    if exists(email):
        raise ValueError(f'Duplicate Username: {email=}')
    if not username:
        raise ValueError('username may not be blank')
    user = {}
    user[NAME] = username
    user[EMAIL] = email
    user[PASSWORD] = dbc.hash_str(password)  # need to hash!
    dbc.connect_db()
    _id = dbc.insert_one(USER_COLLECT, user)
    return str(_id) if _id else "False"


def verify_user(username: str, password: str) -> bool:
    dbc.connect_db()
    if not exists(username):
        raise KeyError(f'No Username exists: {username}')
    # Retrieve user from database using the fetch_one function
    user = dbc.fetch_one(USER_COLLECT, {NAME: username})
    return bcrypt.checkpw(password.encode(), user[PASSWORD].encode())


def update_user(username: str, update_dict: dict):
    dbc.connect_db()
    if not exists(username):
        raise ValueError(f'Update failure: {username} not in database.')
    else:
        ud = update_dict  # preserving update_dict here while hashing password
        if PASSWORD in ud:
            ud = update_dict.copy()
            ud[PASSWORD] = dbc.hash_str(ud[PASSWORD])
        return dbc.update_doc(USER_COLLECT, {NAME: username}, ud)


def del_user(username: str):
    dbc.connect_db()
    if exists(username):
        return dbc.del_one(USER_COLLECT, {NAME: username})
    else:
        raise KeyError(f'User {username} not found.')


def exists(name: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {NAME: name})


def get_user_by_email(email: str):
    """
    Fetches a user from the database by their name.
    """
    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {EMAIL: email})


def get_user_by_name(name: str):
    """
    Fetches a user from the database by their name.
    """
    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {NAME: name})


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
    }

    # Insert the record into the database and retrieve the submission ID
    submission_id = dbc.insert_one(ARTICLE_COLLECTION, submission_record)

    return submission_id


def get_articles_by_username(username):
    """
    Fetch all articles submitted by a specific user identified by username.

    :param username: The username of the user.
    :return: A list of articles submitted by the user.
    """
    # Connect to the database (if not already connected)
    dbc.connect_db()

    # Fetch the user by username to get the user's ID
    user = dbc.fetch_one(USER_COLLECT, {'username': username})
    if not user:
        return None  # User not found

    user_id = user['_id']

    # Fetch all articles submitted by this user
    articles = dbc.fetch_all_with_filter(ARTICLE_COLLECTION,
                                         {USER_ID_FIELD: user_id})

    return articles


def fetch_all_with_filter(collection=ARTICLE_COLLECTION, filt={}):
    """
    Find with a filter and return all matching docs.
    """
    # Connect to the database (if not already connected)
    dbc.connect_db()
    articles = dbc.fetch_all_with_filter(collection, filt)
    # articles = dbc.fetch_all(collection)
    return articles


def update_user_profile(username: str, password: str, update_dict: dict):
    """
    Update a user's profile in the database.

    :param username: The username of the user to be updated.
    :param update_dict: A dictionary containing the fields to be updated.
    """
    # Connect to the database
    dbc.connect_db()

    # check password is correct
    if not verify_user(username, password):
        raise ValueError('Incorrect password.')

    ud = update_dict

    if PASSWORD in ud:
        ud = update_dict.copy()
        ud[PASSWORD] = dbc.hash_str(ud[PASSWORD])

    return dbc.update_doc(USER_COLLECT,
                          {NAME: username},
                          ud)


def clear_user_data(name: str):
    """
    WARNING! THIS REMOVES ALL DATA FROM THE DATABASE!!!
    """

    dbc.connect_db()
    if name != USER_COLLECT:
        raise ValueError(f'Wrong Collection Name, {name}')
    result = dbc.del_all(USER_COLLECT)
    add_user(MOCK_NAME, MOCK_EMAIL, MOCK_PASSWORD)
    del_user(MOCK_NAME)
    return result


def get_all_collection():
    dbc.connect_db()
    return dbc.fetch_collection_name()
