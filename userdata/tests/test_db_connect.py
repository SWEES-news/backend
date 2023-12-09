import pytest

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import db_connect as dbc

TEST_DB = dbc.USER_DB
TEST_COLLECT = 'test_collect'
# can be used for field and value:
TEST_NAME = 'test'
TEST_EMAIL = 'test@gmailcom'
TEST_PASSWORD = 'testword@gmail.com'


@pytest.fixture(scope='function')
def temp_rec():
    temp = dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_NAME: TEST_NAME})
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_NAME: TEST_NAME})

# this fails when fetching string with '.' character in
def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
    assert ret is None
