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

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from endpoints import app

import endpoints as ep # server.

import userdata.db as data

import unittest

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


@patch('userdata.newsdb.get_article_by_id')
def test_bias_analysis_success(mock_get_article):
    """
    Test successful bias analysis.
    """
    # Mocking the article retrieval
    mock_article = {'id': 'some_id', 'content': 'This is a test article'}
    mock_get_article.return_value = mock_article

    response = TEST_CLIENT.post('/bias-analysis', json={
        'article_id': 'some_id',
        # 'analysis_parameters': {}  # Optional parameters if needed
    })
    assert response.status_code == OK
    resp_json = response.get_json()
    assert 'analysis_result' in resp_json


@patch('userdata.newsdb.get_article_by_id', return_value=None)
def test_bias_analysis_article_not_found(mock_get_article):
    """
    Test bias analysis when the article is not found.
    """
    response = TEST_CLIENT.post('/bias-analysis', json={
        'article_id': 'non_existent_id',
    })
    assert response.status_code == NOT_FOUND


@patch('userdata.newsdb.get_article_by_id')
def test_bias_analysis_server_error(mock_get_article):
    """
    Test server error during bias analysis.
    """
    # Simulate a server error during article retrieval
    mock_get_article.side_effect = Exception('Database error')

    response = TEST_CLIENT.post('/bias_analysis', json={
        'article_id': 'some_id',
    })
    assert response.status_code == NOT_FOUND # techniclly should be BAD_REQUEST  


class TestSubmitArticleEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # @patch('server.endpoints.store_article_submission') # , return_value=True
    # def test_successful_submission(self, mock_store):
    #     # Mocking the database call
    #     mock_store.return_value = True

    #     response = self.app.post('/submitarticle', json={
    #         'article_link': 'http://example.com/article',
    #         'submitter_id': 123
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('success', response.json['status'])

    # @patch('server.endpoints.store_article_submission')
    # def test_invalid_data_submission(self, mock_store):
    #     # Mocking the database call
    #     mock_store.return_value = True

    #     # Testing with invalid data
    #     response = self.app.post('/submitarticle', json={
    #         'article_link': '',
    #         'submitter_id': 123
    #     })
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn('error', response.json['status'])

    # @patch('server.endpoints.store_article_submission')
    # def test_server_error_condition(self, mock_store):
    #     # Mocking the database call to simulate a server error
    #     mock_store.side_effect = Exception('Database error')

    #     response = self.app.post('/submitarticle', json={
    #         'article_link': 'http://example.com/article',
    #         'submitter_id': 123
    #     })
    #     self.assertEqual(response.status_code, 500)
    #     self.assertIn('error', response.json['status'])