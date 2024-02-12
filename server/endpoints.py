"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity)
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

api = Api(app)


# ------ Endpoint names ------ #
MAIN_MENU_EP = '/MainMenu'
HELLO_EP = '/hello'
USERS_EP = '/users'
NEWS_LINK_SLASH = '/news'
REMOVE_EP = '/removeUser'
CLEAR_EP = '/ClearUserDataBase'


# ------ Additional strings ------ #
NUM = 0
MENU = 'menu'
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to our site!"
USERS = 'users'
HELLO_STR = 'hello'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'
USER_ID = 'UserID'
NEWS_LINK = 'NewsPage'
NEWS_ID = 'NewsID'
REMOVE_NM = 'Remove User'


@api.route(f'/{HELLO_STR}')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_STR: 'world'}


@api.route('/whoami')
class whoami(Resource):
    """
    The purpose of the whoami endpoint is to get one's public ip address
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with ip addr
        """
        return {'ip': request.remote_addr}


@api.route('/countNumberOfEndpoints')
class countNumberOfEndpoints(Resource):
    """
    The purpose of the whoami endpoint is to get one's public ip address
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with ip addr
        """
        numPoints = len([rule.rule for rule in api.app.url_map.iter_rules()])
        return {'countNumberOfEndpoints': numPoints}


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


@api.route(f'{MAIN_MENU_EP}')
@api.route('/')
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


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all users and adding a user.
    """

    def get(self):
        """
        This method returns all users.
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


@api.route(f'{REMOVE_EP}')
class RemoveUser(Resource):
    @jwt_required()  # ensures valid JWT is present in request headers
    @api.expect(user_model)     # remove_user_model
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'User Not Found')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def post(self):
        """
        Remove/delete a user.
        """

        # Get the identity of current user from JWT
        current_user = get_jwt_identity()
        username = request.json.get(usrs.NAME)

        if current_user != username:
            raise wz.Unauthorized(
                'Unauthorized: You are not authorized to remove this user.')

        try:
            usrs.del_user(username)
        except ValueError:
            raise wz.NotFound('User not found.')

        return {REMOVE_NM: 'User removed successfully.'}


user_login_model = api.model('LoginUser', {
    usrs.NAME: fields.String,
    usrs.PASSWORD: fields.String,
})


@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_login_model)
    @api.response(HTTPStatus.OK, 'Soccessful login')
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


@api.route('/user/<string:name>')   # TODO should we use f'{USERS_EP}/...'
class UserDetail(Resource):            # here instead?
    """
    This class supports fetching details of a specific user.
    """

    def get(self, name):
        """
        This method returns details of a specific user.
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
The /news endpoint serves as a means for users to add to or to
view the list of stored news article links.
When a user selects an article from this list for bias analysis,
they would use a different endpoint,
the /analyze-bias endpoint to submit their request for analysis.
"""


@api.route(f'{NEWS_LINK_SLASH}')
class News(Resource):
    """
    This class supports fetching links to an article
    """
    def get(self):
        """
        This method returns all news article links and name.
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


@api.route('/submit-article')
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
    'article_id':
    fields.String(required=True, description='ID of the article to analyze'),
    'analysis_parameters':
    fields.Raw(required=False, description='Optional parameters for analysis')
})


@api.route('/bias-analysis')
class AnalyzeBias(Resource):
    @api.expect(analyze_bias_model)
    @api.response(HTTPStatus.OK, 'Bias analysis completed')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid request data')
    @api.response(HTTPStatus.NOT_FOUND, 'Article not found')
    def post(self):
        """
        Analyze the bias in a submitted news article.
        """
        data = request.json
        article_id = data.get('article_id')
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
        }

        # return jsonify({
        #     'article_id': article_id,
        #     'analysis_result': analysis_result
        # }), HTTPStatus.OK
        return {
            'article_id': article_id,
            'analysis_result': analysis_result
        }, HTTPStatus.OK


@api.route('/user/<string:username>/articles')
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


@api.route('/get-articles')
class Articles(Resource):
    """
    Gets all articles that have been submitted to the site by all users
    """
    def get(self):
        """
        This method returns all news article links and name.
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


@api.route('/change-username')
class ChangeName(Resource):
    """
    Endpoint to change the username of a user.
    """

    @api.expect(change_username_model)
    def put(self):
        """
        Change the username of a user.
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


@api.route('/change-password')
class ChangePassword(Resource):
    """
    Endpoint to change the password of a user.
    """

    @api.expect(change_password_model)
    def put(self):
        """
        Change the password of a user.
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


@api.route('/change-email')
class ChangeEmail(Resource):
    """
    Endpoint to change the email of a user.
    """

    @api.expect(change_email_model)
    def put(self):
        """
        Change the email of a user.
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
class ClearUserCollection(Resource):
    """
    Removes all elements in a database.
    """

    @api.expect(DatabaseClear)
    def put(self):
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
