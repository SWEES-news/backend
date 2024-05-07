"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import bcrypt
from bson.objectid import ObjectId
from bson.errors import InvalidId

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import userdata.db_connect as dbc


ADMIN_EMAILS = [
    'ethanb@nyu.edu',
    'ethandb2024@gmail.com'
]

# ------ configuration for MongoDB ------ #
USER_COLLECT = 'users'
ARTICLE_COLLECTION = 'articles'
# field name for user ID in the articles collection
SUBMITTER_ID_FIELD = 'submitter_id'
OBJECTID = '_id'

# ------ DB fields ------ #
NAME = 'Username'
EMAIL = 'Email'
PASSWORD = 'Password'
FIRSTNAME = 'FirstName'
LASTNAME = 'LastName'
CONFIRM_PASSWORD = 'confirm_password'

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
    return {OBJECTID: MOCK_ID, NAME: MOCK_NAME, EMAIL: MOCK_EMAIL, PASSWORD: MOCK_PASSWORD}


# returns a randomly generated mock email
def _get_random_name():
    return str(random.randint(0, BIG_NUM))


# returns a randomly generated mock email
def _get_random_email():
    return str(random.randint(0, BIG_NUM - 10)) + EMAIL_TAIL


# gets a user with a random gmail address
def get_rand_test_user():
    rand_part = _get_random_name()
    return {OBJECTID: _gen_id(), NAME: rand_part, PASSWORD: MOCK_PASSWORD, EMAIL: _get_random_email(),
            FIRSTNAME: 'John', LASTNAME: 'Doe', CONFIRM_PASSWORD: MOCK_PASSWORD}


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


def add_user(firstname: str, lastname: str, username: str, email: str, password: str) -> str:
    if exists(username):
        raise ValueError(f'Duplicate Username: {username=}')
    if email_exists(email):
        raise ValueError(f'Duplicate email: {email=}')
    if not username:
        raise ValueError('username may not be blank')
    user = {}
    user[FIRSTNAME] = firstname
    user[LASTNAME] = lastname
    user[NAME] = username
    user[EMAIL] = email
    user[PASSWORD] = dbc.hash_str(password)  # need to hash!
    dbc.connect_db()
    _id = dbc.insert_one(USER_COLLECT, user)
    return str(_id) if _id else "False"


def verify_user(user_id: str, password: str) -> bool:
    dbc.connect_db()
    if not exists_id(user_id):
        data = dbc.fetch_all(USER_COLLECT)
        raise KeyError(f'No user_id exists: {user_id}, {data}')
    # Retrieve user from database using the fetch_one function
    user = dbc.fetch_one(USER_COLLECT, {OBJECTID: user_id})
    return bcrypt.checkpw(password.encode(), user[PASSWORD].encode())


def verify_user_by_name(username: str, password: str) -> bool:
    dbc.connect_db()
    if not exists(username):
        raise KeyError(f'No user exists: {username}')
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


def del_user_by_id(user_id: str):
    dbc.connect_db()
    if exists_id(user_id):
        return dbc.del_one(USER_COLLECT, {OBJECTID: user_id})
    else:
        raise KeyError(f'User {user_id} not found.')


def del_user_by_email(user_email: str):
    dbc.connect_db()
    if get_user_by_email(user_email):
        return dbc.del_many(USER_COLLECT, {EMAIL: user_email})
    else:
        raise KeyError(f'User {user_email} not found.')


def exists(name: str) -> bool:
    dbc.connect_db()
    name = name.lower()
    return dbc.fetch_one(USER_COLLECT, {NAME: name}, False)


def email_exists(email: str) -> bool:
    dbc.connect_db()
    email = email.lower()
    return dbc.fetch_one(USER_COLLECT, {EMAIL: email}, False)


def exists_id(user_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {OBJECTID: user_id})


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


def get_user_by_id(user_id: str) -> dict:
    """
    Fetches a user from the database by their ID.
    """
    if not isinstance(user_id, (str, bytes)):
        raise TypeError(f"Expected user_id to be str or bytes, got {type(user_id)}")

    try:
        # MUST convert the string ID to an ObjectId
        object_id = ObjectId(user_id)
    except InvalidId:
        return None

    dbc.connect_db()
    return dbc.fetch_one(USER_COLLECT, {OBJECTID: object_id})


def fetch_all_with_filter(filt={}):
    """
    Find with a filter and return all matching docs.
    """
    # Connect to the database (if not already connected)
    dbc.connect_db()
    users = dbc.fetch_all_with_filter(USER_COLLECT, filt)
    return users


def update_user_profile(user_id: str, password: str, update_dict: dict):
    """
    Update a user's profile in the database.

    :param username: The username of the user to be updated.
    :param update_dict: A dictionary containing the fields to be updated.
    """

    # Connect to the database
    dbc.connect_db()

    # check password is correct
    if not verify_user(user_id, password):
        raise ValueError('Incorrect password.')

    ud = update_dict

    # The user is attempting to update their password
    # Hash the password if it is being updated
    if PASSWORD in ud:
        ud = update_dict.copy()
        ud[PASSWORD] = dbc.hash_str(ud[PASSWORD])

    return dbc.update_doc(USER_COLLECT,
                          {OBJECTID: user_id},
                          ud)


def clear_data(name: str):
    """
    WARNING! THIS REMOVES ALL ROWS FROM THE DATABASE.
    """

    dbc.connect_db()
    if name not in get_all_collection():
        raise ValueError(f'Collection Does Not Exist: , {name}')
    data = dbc.fetch_all(name)
    if len(data) == 0:
        return name
    element = data[0]
    collection = dbc.del_all(name)
    dbc.insert_one(collection, element)
    dbc.del_first(collection)
    return collection


def get_all_collection():
    dbc.connect_db()
    return dbc.fetch_collection_name()


def get_user_if_logged_in(session):
    """
    Get the user if they are logged in.
    """
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        if user:
            return user[NAME]
        return None
    return None


def has_admin_privilege(user_id):
    """
    Check if the user has admin privilege based on a list of whitelisted emails.
    """
    user = get_user_by_id(user_id)
    if user:
        return user[EMAIL] in ADMIN_EMAILS
    return False
