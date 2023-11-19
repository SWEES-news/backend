import pytest

import userdata.db_connect as dbc

TEST_DB = dbc.USER_DB
TEST_COLLECT = 'test_collect'
# can be used for field and value:
TEST_NAME = 'test'
TEST_EMAIL = 'test@gmail.com'
TEST_PASSWORD = 'testword@gmail.'


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_NAME: TEST_NAME})
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_NAME: TEST_NAME})

# this fails when fetching string with '.' character in
def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    print('\n\n\n\n\n\n\n', ret)
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: 'not a field value in db!'})
    assert ret is None
