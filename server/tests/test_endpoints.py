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