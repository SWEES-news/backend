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
    name = data._get_random_name()
    data.add_user(name, data.MOCK_EMAIL, data.MOCK_PASSWORD)
    yield name
    if data.exists(name):
        data.del_user(name)
    # delete the user!


def test_get_test_name():
    name = data._get_random_name()
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


def test_add_user_dup_name(temp_user):
    """
    Make sure a duplicate user name raises a ValueError.
    """
    dup_name = temp_user
    with pytest.raises(ValueError):
        data.add_user(dup_name, data.MOCK_NAME, data.MOCK_PASSWORD)
    data.del_user(temp_user)


def test_add_user_blank_name():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        data.add_user('', data.MOCK_EMAIL, data.MOCK_PASSWORD)


ADD_NAME = 'newuser'


def test_add_user():
    new_user = data._get_random_name()
    ret = data.add_user(new_user, data.MOCK_EMAIL, data.MOCK_PASSWORD)
    assert data.exists(new_user)
    assert ret is not None
    data.del_user(new_user)


def test_update_user(temp_user):
    NEW_NAME = data.MOCK_NAME_2
    NEW_EMAIL = data.MOCK_EMAIL_2
    NEW_PASSWORD = data.MOCK_PASSWORD_2

    old_user_name = temp_user

    new_user_info = {
        data.NAME: NEW_NAME,
        data.EMAIL: NEW_EMAIL,
        data.PASSWORD: NEW_PASSWORD,
    }

    data.update_user(old_user_name, new_user_info)
    assert data.exists(NEW_NAME)
    assert not data.exists(old_user_name)
    updated_user = data.get_user_by_name(NEW_NAME)
    assert updated_user[data.EMAIL] == NEW_EMAIL
    assert updated_user[data.PASSWORD] == NEW_PASSWORD
    data.del_user(NEW_NAME) # have to do this because info changed

def test_del_user(temp_user):
    name = temp_user
    data.del_user(name)
    assert not data.exists(name)


def test_del_user_not_there():
    name = data._get_random_name()
    with pytest.raises(ValueError):
        data.del_user(name)