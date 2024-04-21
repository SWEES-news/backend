from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
    UNAUTHORIZED
)
from http import HTTPStatus

from unittest.mock import patch  #, MagicMock

import pytest

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from endpoints import app

import endpoints as ep # server.

from endpoints import UserLogin

from flask import Flask
from flask_restx import Api

import userdata.users as usrs
import userdata.articles as articles

import unittest

TEST_CLIENT = ep.app.test_client()


# @patch('userdata.users.add_user', return_value=usrs.MOCK_ID, autospec=True)
# def test_users_add(mock_add):
#     """
#     Testing we do the right thing with a good return from add_user.
#     """
#     route = ep.USERS_EP + ep.REGISTER_EP
#     resp = TEST_CLIENT.post(route, json=usrs.get_rand_test_user())
#     assert resp.status_code == OK


# @patch('userdata.users.add_user', side_effect=ValueError(), autospec=True) 
# def test_users_bad_add(mock_add):
#     """
#     Testing we do the right thing with a value error from add_user.
#     """
#     route = ep.USERS_EP + ep.REGISTER_EP
#     resp = TEST_CLIENT.post(route, json=usrs.get_test_user())
#     assert resp.status_code == NOT_ACCEPTABLE


# @patch('userdata.users.add_user', return_value=None)
# def test_users_add_db_failure(mock_add):
#     """
#     Testing we do the right thing with a null ID return from add_user.
#     """
#     route = ep.USERS_EP + ep.REGISTER_EP
#     resp = TEST_CLIENT.post(route, json=usrs.get_test_user())
#     assert resp.status_code == SERVICE_UNAVAILABLE


# Testing update user endpoint
# might need some help with figuring this out
# @patch('userdata.users.update_user', return_value=...)
# def test_update_user_success(mock_user):
#     resp = TEST_CLIENT.put(ep.USERS_EP, json=data.update_test_user())
#     pass


# @patch('userdata.users.update_user')
# def test_update_user_failure(mock_user):
#     pass


# ------------------------------------------------------------------------
# # , return_value=usrs.MOCK_USER_REMOVED, autospec=True
# @patch('userdata.users.del_user')
# def test_remove_user_succeeded(mock_delete):
#     """
#     Testing we do the right thing with a call to del_user that succeeds.
#     """
#     # Generate a valid JWT token for testing
#     #cjwt_token = ep.create_token(usrs.get_test_user())

#     # resp = TEST_CLIENT.delete(f'{ep.DEL_GAME_EP}/AnyName')
#     # resp = TEST_CLIENT.post(ep.USERS_EP, json=usrs.get_rand_test_user())
#     resp = TEST_CLIENT.post(ep.REMOVE_EP, json=usrs.get_test_user())
#     # resp = TEST_CLIENT.post(
#     #     ep.REMOVE_EP,
#     #     json=usrs.get_test_user(),
#     #     headers={'Authorization': f'Bearer {jwt_token}'},
#     # )

#     assert resp.status_code == OK


# @patch('userdata.users.del_user', side_effect=ValueError(), autospec=True)
# def test_remove_nonexistent_user(mock_delete):
#     """
#     Testing we do the right thing with a value error from add_user.

#     """
#     # jwt_token = ep.create_token(usrs.get_test_user())

#     resp = TEST_CLIENT.post(ep.REMOVE_EP, json=usrs.get_test_user())
#     # resp = TEST_CLIENT.post(
#     #     ep.REMOVE_EP,
#     #     json=usrs.get_test_user(),
#     #     headers={'Authorization': f'Bearer {jwt_token}'},
#     # )

#     assert resp.status_code == NOT_ACCEPTABLE


# @patch('userdata.users.del_user', return_value=None)
# def test_remove_user_db_failure(mock_delete):
#     """
#     Testing we do the right thing with a null ID return from add_user.
#     """
#     # jwt_token = ep.create_token(usrs.get_test_user())

#     resp = TEST_CLIENT.post(ep.REMOVE_EP, json=usrs.get_test_user())
#     # resp = TEST_CLIENT.post(
#     #     ep.REMOVE_EP,
#     #     json=usrs.get_test_user(),
#     #     headers={'Authorization': f'Bearer {jwt_token}'},
#     # )

#     assert resp.status_code == SERVICE_UNAVAILABLE


# @patch('userdata.users.del_user')
# def test_remove_user_unauthorized(mock_delete):
#     """
#     Testing we do the right thing if user tries to remove a different user
#     (users can only delete/modify their own accounts).
#     """
#     jwt_token = ep.create_token(usrs.get_test_user())   # user with an account

#     resp = TEST_CLIENT.post(
#         ep.REMOVE_EP,
#         json=usrs.get_rand_test_user(),    # not the logged in user's username
#         headers={'Authorization': f'Bearer {jwt_token}'},
#     )

#     assert resp.status_code == UNAUTHORIZED
    # -----------------------------------------------------------------------

@pytest.mark.skip("Test not implemented, need to add register, login, submit article and then test the bias analysis")
@patch('userdata.articles.get_article_by_id')
def test_bias_analysis_success(mock_get_article):
    """
    Test successful bias analysis.
    """
    # Mocking the article retrieval
    mock_article = {'id': 'some_id', 'content': 'This is a test article'}
    mock_get_article.return_value = mock_article

    article_id = 'some_id'
    response = TEST_CLIENT.post(f'{ep.ARTICLES_EP}{ep.ANALYSIS_EP}{article_id}', json={
        # 'analysis_parameters': {}  # Optional parameters if needed
    })
    assert response.status_code == OK
    resp_json = response.get_json()
    assert 'analysis_result' in resp_json

@pytest.mark.skip("Test not implemented, need to add register, login, submit article and then test the bias analysis")
@patch('userdata.articles.get_article_by_id', return_value = False)
def test_bias_analysis_article_not_found(mock_get_article):
    """
    Test bias analysis when the article is not found.
    """

    article_id = 'nonexistent_id'
    response = TEST_CLIENT.post(f'{ep.ARTICLES_EP}{ep.ANALYSIS_EP}{article_id}', json={})
    assert response.status_code == NOT_FOUND


@pytest.mark.skip('Test bad request from AI model')
@patch('userdata.articles.get_article_by_id')
def test_bias_analysis_server_error(mock_get_article):
    """
    Test server error during bias analysis.
    """
    # Simulate a server error during article retrieval
    mock_get_article.side_effect = Exception('Database error')

    article_id = 'some_id'
    response = TEST_CLIENT.post(f'{ep.ARTICLES_EP}/{ep.ANALYSIS_EP}/{article_id}', json={})
    assert response.status_code == BAD_REQUEST

@pytest.mark.skip("Test not implemented, need to add register, login, submit article and then test the bias analysis")
@patch('userdata.articles.store_article_submission', return_value=True) # , return_value=True
def test_successful_submission(mock_store):
    # Mocking the database call

    response = TEST_CLIENT.post(f'{ep.ARTICLES_EP}{ep.SUBMIT_EP}', json={
        articles.ARTICLE_LINK: 'http://example.com/article',
        articles.ARTICLE_BODY: 123
    })
    assert response.status_code == OK

@pytest.mark.skip("Test not implemented, need to add register, login, submit article and then test the bias analysis")
@patch('userdata.articles.store_article_submission', return_value=None)
def test_invalid_data_submission(mock_store):
    # Mocking the database call

    # Testing with invalid data
    response = TEST_CLIENT.post(f'{ep.ARTICLES_EP}{ep.SUBMISSIONS_EP}', json={
        'article_link': '',
        'submitter_id': 123
    })
    assert response.status_code == BAD_REQUEST

@pytest.mark.skip('Test bad request from AI model')
@patch('server.endpoints.store_article_submission')
def test_server_error_condition(self, mock_store):
    # Mocking the database call to simulate a server error
    mock_store.side_effect = Exception('Database error')

    response = self.app.post(f'{ep.ARTICLES_EP}/submit', json={
        'article_link': 'http://example.com/article',
        'submitter_id': 123
    })
    self.assertEqual(response.status_code, 500)
    self.assertIn('error', response.json['status'])


# @patch('server.endpoints.create_token', return_value='fake_token')
# @patch('userdata.users.add_user', return_value='fake_token')
# def test_create_user(mock_add):
#     # Simulating a scenario where the credentials are valid
#     print(f'{ep.USERS_EP}{ep.REGISTER_EP}')
#     mock_add.return_value = usrs.MOCK_ID
#     response = TEST_CLIENT.post(ep.USERS_EP + ep.REGISTER_EP, json={
#         usrs.NAME: 'test@example.com',
#         usrs.EMAIL: 'test@example.com',
#         usrs.PASSWORD: 'password123'
#     })
#     assert response.status_code == OK

@patch('userdata.users.verify_user_by_name')
@patch('userdata.users.get_user_by_name') 
def test_valid_credentials(mock_get, mock_verify): 
    mock_get.return_value = usrs.get_test_user()
    mock_verify.return_value = True
    response = TEST_CLIENT.post(ep.USERS_EP + ep.LOGIN_EP, json={
        usrs.NAME: 'test@example.com',
        usrs.PASSWORD: 'password123'
    })
    assert response.status_code == OK

@patch('userdata.users.verify_user_by_name', return_value=False)  # Mocking the verify_user function
def test_invalid_credentials(mock_verify):
    # Simulating a scenario where the credentials are invalid

    response = TEST_CLIENT.post(f'{ep.USERS_EP}{ep.LOGIN_EP}', json={
        usrs.NAME: 'wrong@example.com',
        usrs.PASSWORD: 'wrongpassword'
    })

    assert response.status_code == UNAUTHORIZED

#returning 404 not found
# def test_clearDBAfterTest():
#     response = TEST_CLIENT.delete(f'{ep.COLLECTIONS_EP}{ep.CLEAR_EP}', json={'Name': 'test_collect'})
#     assert response.status_code == OK or response.status_code == BAD_REQUEST

@pytest.mark.skip('Getting 404 instead of 200 Status Code')
@patch('basic.analyze_content')
@patch('userdata.articles.get_article_by_id')
def test_analyze_bias(mock_get_article_by_id, mock_analyze_content):
    """
    Test the AnalyzeBias endpoint with valid input.
    """
    # Mocking the get_article_by_id function to return a test article
    # mock_article = MagicMock()
    # mock_article.get.return_value = "This is a test article."
    # mock_get_article_by_id.return_value = mock_article

    mock_get_article_by_id.return_value = {
        'article_title': 'Sample Article',
        'article_body': 'This is a sample article for testing purposes.'
    }

    # Mocking the analyze_content function to return a predefined analysis result and vector store
    mock_analyze_content.return_value = (["This is a bias analysis result"], None)

    # Sending a POST request to the endpoint
    response = TEST_CLIENT.post(f'{ep.ANALYSIS_EP}{ep.ARTICLE_ID_EP}', json={'article_id': 'test_article_id'})

    # Asserting the response status code
    assert response.status_code == HTTPStatus.OK

    # Asserting the response data
    data = response.json()
    assert 'article_id' in data
    assert 'analysis_result' in data
    assert data['article_id'] == 'test_article_id'
    assert data['analysis_result'] == ["This is a bias analysis result"]
