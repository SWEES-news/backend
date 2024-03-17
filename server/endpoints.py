"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_jwt_extended import (create_access_token)  # ,
#                                # jwt_required, get_jwt_identity)
from flask_cors import CORS

import werkzeug.exceptions as wz

import os
import sys
import inspect
import userdata.users as usrs
import userdata.newsdb as news
from userdata.users import store_article_submission

# ------ DB fields ------ # For endpoints that change user data
NAME = 'Username'
EMAIL = 'Email'
PASSWORD = 'Password'

# Modifying sys.path to include parent directory for local imports
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

app = Flask(__name__)
CORS(app)

api = Api(app, title='SWEES API', default='extras')

# namespaces
# example

us = api.namespace('user',
                   description="operations for users")
ar = api.namespace('articles',
                   description="operations for user-submitted articles")
an = api.namespace('analysis',
                   description="operations for analyzing article bias")
# ns = api.Namespace('basic stuff', description="this is basic stuff")
# use ns.route instead of api.route

# ------ Endpoint names ------ #
USERS_EP = f'/{us.name}'
ARTICLES_EP = f'/{ar.name}'
ANALYSIS_EP = f'/{an.name}'

MAIN_MENU_EP = '/MainMenu'
REMOVE_EP = '/remove'
CLEAR_EP = '/Collection'

# ------ Additional strings ------ #
NUM = 0
MENU = 'menu'
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to our site!"
USERS = 'users'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'
USER_ID = 'UserID'
NEWS_LINK = 'NewsPage'
NEWS_ID = 'NewsID'
REMOVE_NM = 'Remove User'


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route('/', f'{MAIN_MENU_EP}')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {'Title': MAIN_MENU_NM,
                'Default': 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Games'},
                    '3': {'url': f'/{USERS}',
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
                }}


user_model = api.model('NewUser', {
    usrs.NAME: fields.String,
    usrs.EMAIL: fields.String,
    usrs.PASSWORD: fields.String,
})


@us.route('')
class Users(Resource):
    """
    Get a list of all users, or add users.
    """

    def get(self):
        """
        Get all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: usrs.get_users(),
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(user_model)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        name = request.json[usrs.NAME]
        email = request.json[usrs.EMAIL]
        password = request.json[usrs.PASSWORD]

        try:
            new_id = usrs.add_user(name, email, password)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')

            return {USER_ID: new_id}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


def create_token(username):
    print('in create token')
    return create_access_token(identity=username)


@us.route(f'{REMOVE_EP}')
class RemoveUser(Resource):
    # @jwt_required()  # ensures valid JWT is present in request headers
    @api.expect(user_model)     # remove_user_model
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'User Not Found')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def delete(self):
        """
        Remove/delete a user.
        """
        username = request.json.get(usrs.NAME)
        password = request.json.get(usrs.PASSWORD)
        try:
            if usrs.verify_user(username, password):
                usrs.del_user(username)
            else:
                raise ValueError()
        except KeyError:
            raise wz.NotFound('User not found.')
        except ValueError:
            raise wz.Unauthorized('Password incorrect.')

        return {REMOVE_NM: 'User removed successfully.'}


user_login_model = api.model('LoginUser', {
    usrs.NAME: fields.String,
    usrs.PASSWORD: fields.String,
})


@us.route('/login')
class UserLogin(Resource):
    @api.expect(user_login_model)
    @api.response(HTTPStatus.OK, 'Successful login')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Falled to login')
    def post(self):
        name = request.json[NAME]
        password = request.json[PASSWORD]
        try:
            verify = usrs.verify_user(name, password)
            if not verify or verify is None:
                raise wz.Unauthorized('Falled to login')
        except ValueError as e:
            raise wz.Unauthorized(f'{str(e)}')


@us.route('/<string:name>')
class UserDetail(Resource):
    """
    Fetch details of a specific user.
    """

    def get(self, name):
        """
        Get details of a specific user.
        """
        user = usrs.get_user_by_name(name)
        if user:
            return user
        else:
            api.abort(HTTPStatus.NOT_FOUND, f'User w/ name \'{name}\''
                      ' not found')


news_model = api.model('NewArticle', {
    news.NAME: fields.String,
    news.LINK: fields.Integer,
})


"""
The /articles endpoint (ar) serves as a means for users to add to or to
view the list of stored news article links.
When a user selects an article from this list for bias analysis,
they would use a different endpoint,
the /analysis endpoint (an) to submit their request for analysis.
"""


@ar.route('')
class News(Resource):
    """
    This class supports fetching links to an article
    """
    def get(self):
        """
        Get all news article links and name.
        """
        return {
            TYPE: DATA,
            TITLE: 'Stored Articles',
            DATA: news.get_articles(),
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(news_model)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a news link.
        """
        name = request.json[news.NAME]
        link = request.json[news.LINK]

        try:
            new_id = news.add_article(name, link)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {NEWS_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


submit_article_model = api.model('SubmitArticle', {
    'article_link': fields.String,
    'submitter_id': fields.String,
})


@ar.route('/submit')
class SubmitArticle(Resource):
    @api.expect(submit_article_model)
    @api.response(HTTPStatus.OK, 'Article submitted successfully')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid data')
    def post(self):
        """
        Submit an article for review.
        """
        article_link = request.json['article_link']
        submitter_id = request.json['submitter_id']

        # Validate the input data
        if not article_link or not submitter_id:
            api.abort(
                HTTPStatus.BAD_REQUEST,
                "Invalid data: 'article_link' and 'submitter_id' are required"
            )

        # Implement logic to store the article submission for review.
        # For example, you might save it to a database.
        submission_id = store_article_submission(article_link, submitter_id)

        if submission_id is None:
            raise wz.NotAcceptable(f'{str(submission_id)} Not Found')
        return (
            {
                "message": "Article submitted successfully",
                "submission_id": str(submission_id)  # causes a 500
            },
        )


# Define the request model for bias analysis
analyze_bias_model = api.model('AnalyzeBias', {
    # 'article_id':
    # fields.String(required=True, description='ID of the article to analyze'),
    'analysis_parameters':
    fields.Raw(required=False, description='Optional parameters for analysis')
})


@an.route('/<string:article_id>')
class AnalyzeBias(Resource):
    @api.expect(analyze_bias_model)
    @api.response(HTTPStatus.OK, 'Bias analysis completed')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid request data')
    @api.response(HTTPStatus.NOT_FOUND, 'Article not found')
    def post(self, article_id):
        """
        Analyze the bias in a submitted news article.
        """
        # data = request.json
        # analysis_parameters = data.get('analysis_parameters', {})

        # Use the provided function to retrieve the article by its ID
        article = news.get_article_by_id(article_id)
        if not article:
            api.abort(HTTPStatus.NOT_FOUND,
                      f'Article with ID {article_id} not found')

        # Perform bias analysis (pseudo-code)
        try:
            # analysis_result = analyze_article_bias(article,
            # analysis_parameters)
            pass
        except Exception as e:
            api.abort(HTTPStatus.BAD_REQUEST,
                      f'Article with ID {article_id} could not be analyzed'
                      f' due to error: {e}')

        # For demonstration, we'll return a dummy response
        analysis_result = {
            'bias_level': 'moderate',
            'bias_type': ['political', 'emotional'],
            'detailed_analysis': '...'
        }  # should send this in get, not post, once we clean up

        return {
            'article_id': article_id,
            'analysis_result': analysis_result
        }, HTTPStatus.OK


@ar.route('/<string:username>')
class UserArticles(Resource):
    """
    Endpoint to retrieve articles submitted by a specific user.
    """

    def get(self, username):
        """
        Return a list of articles submitted by the given user.
        """
        try:
            articles = usrs.get_articles_by_username(username)

            return {
                'username': username,
                'articles': articles
            }, HTTPStatus.OK

        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@ar.route('/all')
class Articles(Resource):
    """
    Gets all articles that have been submitted to the site by all users
    """
    def get(self):
        """
        Get all news article links and titles.
        """
        return {
            TYPE: DATA,
            TITLE: 'Stored Articles',
            DATA: usrs.fetch_all_with_filter(),
            RETURN: MAIN_MENU_EP,
        }


change_username_model = api.model('ChangeUsername', {
    'old_username': fields.String(
        required=True, description='The current username'),
    'new_username': fields.String(
        required=True, description='The new username'),
    'password': fields.String(
        required=True, description='Confirmation of the  password')
})


@us.route('/username')
class ChangeName(Resource):
    """
    Endpoint to update the username of a user.
    """

    @api.expect(change_username_model)
    def put(self):
        """
        Update theusername of a user.
        """
        response = request.json
        old_username = response.get('old_username')
        new_username = response.get('new_username')
        password = response.get('password')

        try:
            if usrs.get_user_by_name(new_username):
                return {'message': 'Username already exists.'}, \
                    HTTPStatus.BAD_REQUEST
            usrs.update_user_profile(old_username, password,
                                     {NAME: new_username})
            return {'message': 'Username changed successfully.'}, \
                HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


change_password_model = api.model('ChangePassword', {
    'username': fields.String(
        required=True, description='The username'),
    'old_password': fields.String(
        required=True, description='The current password'),
    'new_password': fields.String(
        required=True, description='The new password'),
    'confirm_new_password': fields.String(
        required=True, description='Confirmation of the new password')
})


@us.route('/password')
class ChangePassword(Resource):
    """
    Endpoint to update the password of a user.
    """

    @api.expect(change_password_model)
    def put(self):
        """
        Update the password of a user.
        """
        response = request.json
        username = response.get('username')
        old_password = response.get('old_password')
        new_password = response.get('new_password')

        if response.get('new_password') != \
                response.get('confirm_new_password'):
            return {'message': 'Passwords do not match.'}, \
                   HTTPStatus.BAD_REQUEST

        try:
            usrs.update_user_profile(username, old_password,
                                     {PASSWORD: new_password})
            return {'message': 'Password changed successfully.'}, \
                HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


change_email_model = api.model('ChangeEmail', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='current password'),
    'new_email': fields.String(required=True, description='new email')
})


@us.route('/email')
class ChangeEmail(Resource):
    """
    Endpoint to update the email of a user.
    """

    @api.expect(change_email_model)
    def put(self):
        """
        Update the email of a user.
        """
        response = request.json
        username = response.get('username')
        password = response.get('password')
        new_email = response.get('new_email')

        try:
            usrs.update_user_profile(username, password,
                                     {EMAIL: new_email})
            return {'message': 'EMAIL changed successfully.'}, \
                HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST


DatabaseClear = api.model('Database Name', {
    'Name': fields.String(required=True, description='Database'),
})


@api.route(CLEAR_EP)
class Collection(Resource):
    @api.expect(DatabaseClear)
    def delete(self):
        """
        Clears the User Database.
        """
        response = request.json
        name = response.get('Name')

        try:
            usrs.clear_user_data(name)
            return {'message': 'Database Cleared'}, \
                HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST

    def get(self):
        """
        Get the name of every collection.
        """
        return {
            TYPE: DATA,
            TITLE: 'collection name',
            DATA: usrs.get_all_collection(),
            RETURN: MAIN_MENU_EP,
        }
