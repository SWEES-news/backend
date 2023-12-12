import pytest

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import db as data
# import userdata.db_connect as dbc

@pytest.fixture(scope='function')
def temp_user():
    email = data._get_random_email()
    ret = data.add_user(email, data.MOCK_NAME, data.MOCK_PASSWORD)
    return email
    # delete the user!


def test_get_test_email():
    name = data._get_random_email()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = data._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == data.ID_LEN


def test_get_test_user():
    assert isinstance(data.get_rand_test_user(), dict)


def test_get_users(temp_user):
    users = data.get_users()
    assert isinstance(users, dict)
    # assert len(users) > 0
    for user in users:
        assert isinstance(user, str)
        assert isinstance(users[user], dict)
    assert temp_user in users
    data.del_user(temp_user)


def test_add_user_dup_email(temp_user):
    """
    Make sure a duplicate user email raises a ValueError.
    """
    dup_name = temp_user
    with pytest.raises(ValueError):
        data.add_user(dup_name, data.MOCK_NAME, data.MOCK_PASSWORD)
    data.del_user(temp_user)


def test_add_user_blank_email():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        data.add_user('', data.MOCK_NAME, data.MOCK_PASSWORD)


ADD_EMAIL = 'newuser@gmail.com'


def test_add_user():
    new_user = data._get_random_email()
    ret = data.add_user(new_user, data.MOCK_NAME, data.MOCK_PASSWORD)
    assert data.exists(new_user)
    assert ret is not None
    data.del_user(new_user)

def test_del_user(temp_user):
    email = temp_user
    data.del_user(email)
    assert not data.exists(email)


def test_del_user_not_there():
    name = data._get_random_email()
    with pytest.raises(ValueError):
        data.del_user(name)