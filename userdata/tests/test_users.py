import pytest

import os
import sys
import inspect
import bcrypt

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import userdata.users as usrs
from userdata.db_connect import hash_str
# import userdata.db_connect as dbc

@pytest.fixture(scope='function')
def temp_user():
    name = usrs._get_random_name()
    usrs.add_user(name, usrs.MOCK_EMAIL, usrs.MOCK_PASSWORD)
    yield name
    if usrs.exists(name):
        usrs.del_user(name)
    # delete the user!


def test_get_test_name():
    name = usrs._get_random_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = usrs._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == usrs.ID_LEN


def test_get_test_user():
    assert isinstance(usrs.get_rand_test_user(), dict)


def test_get_users(temp_user):
    users = usrs.get_users()
    assert isinstance(users, dict)
    # assert len(users) > 0
    for user in users:
        assert isinstance(user, str)
        assert isinstance(users[user], dict)
    assert temp_user in users


def test_verify_user(temp_user):
    v = usrs.verify_user(temp_user, usrs.MOCK_PASSWORD)
    assert v


def test_verify_user_wrong_password(temp_user):
    assert not usrs.verify_user(temp_user, usrs.MOCK_PASSWORD_2)


def test_verify_user_wrong_username():
    with pytest.raises(KeyError):
        usrs.verify_user('', usrs.MOCK_PASSWORD)


def test_add_user_dup_name(temp_user):
    """
    Make sure a duplicate user name raises a ValueError.
    """
    dup_name = temp_user
    with pytest.raises(ValueError):
        usrs.add_user(dup_name, usrs.MOCK_NAME, usrs.MOCK_PASSWORD)

def test_clear_collection_wrong_name():
    """
    Makes sure protection from clearing database works
    """
    with pytest.raises(ValueError):
        usrs.clear_user_data("Wrong Name")

def test_add_user_blank_name():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        usrs.add_user('', usrs.MOCK_EMAIL, usrs.MOCK_PASSWORD)


ADD_NAME = 'newuser'


def test_add_user():
    new_user = usrs._get_random_name()
    ret = usrs.add_user(new_user, usrs.MOCK_EMAIL, usrs.MOCK_PASSWORD)
    assert usrs.exists(new_user)
    assert ret is not None


def test_update_user(temp_user):
    NEW_NAME = usrs.MOCK_NAME_2
    NEW_EMAIL = usrs.MOCK_EMAIL_2
    NEW_PASSWORD = usrs.MOCK_PASSWORD_2

    old_user_name = temp_user

    new_user_info = {
        usrs.NAME: NEW_NAME,
        usrs.EMAIL: NEW_EMAIL,
        usrs.PASSWORD: NEW_PASSWORD,
    }

    usrs.update_user(old_user_name, new_user_info)
    assert usrs.exists(NEW_NAME)
    assert not usrs.exists(old_user_name)
    updated_user = usrs.get_user_by_name(NEW_NAME)
    assert updated_user[usrs.EMAIL] == NEW_EMAIL
    assert bcrypt.checkpw(NEW_PASSWORD.encode(), updated_user[usrs.PASSWORD].encode()) # updated_user[usrs.PASSWORD] == hash_str(NEW_PASSWORD)
    usrs.del_user(NEW_NAME) # have to do this because info changed


def test_del_user(temp_user):
    name = temp_user
    usrs.del_user(name)
    assert not usrs.exists(name)


def test_del_user_not_there():
    name = usrs._get_random_name()
    with pytest.raises(KeyError):
        usrs.del_user(name)
