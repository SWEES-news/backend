from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

import server.endpoints as ep

import userdata.db as data

TEST_CLIENT = ep.app.test_client()

# tests if the hello world endpoint, which indicates if server is running at all
def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_SLASH)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_STR in resp_json

# checks the users
@pytest.mark.skip('this test does not work since we are switching from API')
def test_list_users():
    resp = TEST_CLIENT.get(ep.Users_SLASH)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert len(resp_json) > 0


@patch('userdata.db.add_user', return_value=data.MOCK_ID, autospec=True)
def test_users_add(mock_add):
    """
    Testing we do the right thing with a good return from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_SLASH, json=data.get_rand_test_user())
    assert resp.status_code == OK


@patch('userdata.db.add_user', side_effect=ValueError(), autospec=True) 
def test_games_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_SLASH, json=data.get_test_user())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('userdata.db.add_user', return_value=None)
def test_games_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_SLASH, json=data.get_test_user())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('userdata.db.get_user_by_id')
def test_user_detail_success(mock_get_user):
    mock_user = {
        'name': 'John Doe',
        'email': 'john@example.com',
        # ... other user fields ...
    }
    mock_get_user.return_value = mock_user
    user_id = 1  # Assuming 1 is a valid user ID for the test
    resp = TEST_CLIENT.get(f'/user/{user_id}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert 'name' in resp_json  # Replace 'name' with the actual fields you expect

@patch('userdata.db.get_user_by_id', return_value=None)
def test_user_detail_not_found(mock_get_user):
    user_id = 999  # Assuming 999 is an invalid user ID for the test
    resp = TEST_CLIENT.get(f'/user/{user_id}')
    assert resp.status_code == NOT_FOUND

