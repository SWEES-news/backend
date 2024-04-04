"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from flask import Flask, request, session
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS
from http import HTTPStatus
import werkzeug.exceptions as wz

import os
import sys
import inspect
import userdata.users as users
import userdata.articles as articles

# Modifying sys.path to include parent directory for local imports
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'h-J_l62fxF1uDXqKjHS3EQ')  # secure asf
cors = CORS(app, supports_credentials=True, resources={r"*": {"origins": "http://localhost:3000"}})

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

# ------ Namespace names ------ #
USERS_EP = f'/{us.name}'
ARTICLES_EP = f'/{ar.name}'

# ------ Endpoint names ------ #
ACCOUNT_EP = '/account'
REGISTER_EP = '/register'
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
UPDATE_USERNAME_EP = '/update/username'
UPDATE_PASSWORD_EP = '/update/password'
UPDATE_EMAIL_EP = '/update/email'
DELETE_EP = '/update/DeleteAccount'
STATUS_EP = '/status'
SUBMIT_EP = '/submit'
SUBMISSIONS_EP = '/submissions'
ANALYSIS_EP = '/submissions/analysis'
ENDPOINTS_EP = '/endpoints'

MAIN_MENU_EP = '/MainMenu'
CLEAR_EP = '/Collection'
USER_NAME_EP = '/<string:name>'
ALL_EP = '/all'
ARTICLE_ID_EP = '/<string:article_id>'

"""
Add endpoint to delete articles
Only delete article if Link was not provided
"""

# ------ Additional strings ------ #
NUM = 0
MENU = 'menu'
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to our site!"
USERS = 'users'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
USER = 'User'
RETURN = 'Return'


@api.route(ENDPOINTS_EP)
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
    users.NAME: fields.String,
    users.EMAIL: fields.String,
    users.PASSWORD: fields.String,
})


@us.route('')
class Users(Resource):
    """
    Get a list of all users. DEBUG REMOVE FROM PROD.
    """

    def get(self):
        """
        Get a list of all users. DEBUG REMOVE FROM PROD.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: users.get_users(),
            RETURN: MAIN_MENU_EP,
        }


@us.route(ACCOUNT_EP)
class UserAccount(Resource):
    def get(self):
        """
        Get the account information of the currently logged in user.
        """
        if 'user_id' in session:
            user = users.get_user_by_id(session['user_id'])
            return {
                TYPE: DATA,
                TITLE: 'Account Information',
                DATA: user,
                USER: users.get_user_if_logged_in(session),
                RETURN: MAIN_MENU_EP,
            }
        else:
            return {'message': 'No user currently logged in'}, HTTPStatus.UNAUTHORIZED


@us.route(REGISTER_EP)
class RegisterUser(Resource):
    @api.expect(user_model)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        name = request.json[users.NAME]
        email = request.json[users.EMAIL]
        password = request.json[users.PASSWORD]

        try:
            new_id = users.add_user(name, email, password)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')

            return {users.OBJECTID: new_id}

        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@us.route(DELETE_EP)
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
        username = request.json.get(users.NAME)
        password = request.json.get(users.PASSWORD)
        try:
            if users.verify_user(username, password):
                users.del_user(username)
            else:
                raise ValueError()
        except KeyError:
            raise wz.NotFound('User not found.')
        except ValueError:
            raise wz.Unauthorized('Password incorrect.')

        return {'UPDATE': 'User removed successfully.'}


user_login_model = api.model('LoginUser', {
    users.NAME: fields.String(required=True, min_length=3, max_length=25, description='User Name'),
    users.PASSWORD: fields.String(required=True, min_length=4, description='Password')
})


@us.route(LOGIN_EP)
class UserLogin(Resource):
    @api.expect(user_login_model)
    @api.response(HTTPStatus.OK, 'Successful login')
    @api.response(HTTPStatus.NOT_FOUND, 'Not a valid username')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Wrong password')
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(users.NAME, type=str, required=True, help='Username cannot be blank', location='json')
        parser.add_argument(users.PASSWORD, type=str, required=True, help='Password cannot be blank', location='json')
        args = parser.parse_args()
        print(args.items())
        username = args[users.NAME]
        password = args[users.PASSWORD]
        try:
            if users.verify_user(username, password):
                user_id = users.get_user_by_name(username)[users.OBJECTID]
                session['user_id'] = user_id
                return {
                    DATA: 'Login successful',
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.OK
            else:
                raise wz.Unauthorized('Falled to login')
        except (ValueError, KeyError) as e:
            raise wz.Unauthorized(f'{str(e)}')


@us.route(LOGOUT_EP)
class UserLogout(Resource):
    def get(self):
        if 'user_id' in session:
            userid = session['user_id']
            session.pop('user_id')
            username = users.get_user_by_id(userid)[users.NAME]
            return {'message': f'Logged out {username}'}, HTTPStatus.OK
        else:
            return {'message': 'No user currently logged in'}, HTTPStatus.BAD_REQUEST


@us.route(USER_NAME_EP)
class UserDetail(Resource):
    """
    Fetch details of a specific user.
    """

    def get(self, name):
        """
        Get details of a specific user. Remove from Prod.
        """
        user = users.get_user_by_name(name)
        if user:
            return user
        else:
            api.abort(HTTPStatus.NOT_FOUND, f'User w/ name \'{name}\''
                      ' not found')


@us.route(STATUS_EP)
class LoggedIn(Resource):
    def get(self):
        """
        Check if a user is currently logged in.
        """
        if 'user_id' in session:
            print(session)
            return {
                USER: users.get_user_if_logged_in(session)
                }, HTTPStatus.OK
        else:
            return {
                DATA: 'No user currently logged in',
                USER: 'None'
                }, HTTPStatus.UNAUTHORIZED


submit_article_model = api.model('SubmitArticle', {
    articles.ARTICLE_LINK: fields.String(required=True, description='Link to the article'),
    articles.ARTICLE_TITLE: fields.String(required=True, description='Title this article'),
})


@ar.route(ALL_EP)
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
            DATA: articles.fetch_all(),
            RETURN: MAIN_MENU_EP,
        }


submit_article_model = api.model('SubmitArticle', {
    articles.ARTICLE_LINK: fields.String(description='Link to the article'),
    articles.ARTICLE_BODY: fields.String(description='Body of the article'),
    articles.ARTICLE_TITLE: fields.String(required=True, description='Title of the article'),
})


@ar.route(SUBMIT_EP)
class SubmitArticle(Resource):
    @api.expect(submit_article_model)
    @api.response(HTTPStatus.OK, 'Article submitted successfully')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid data')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized access')
    def post(self):
        """
        Submit an article for review.
        Must submit either a link or a body of text, or both.
        """
        if 'user_id' not in session:
            return {DATA: 'No user currently logged in'}, HTTPStatus.UNAUTHORIZED
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(articles.ARTICLE_LINK, type=str, required=False,
                            help='Article link cannot be blank if article body is also blank.')
        parser.add_argument(articles.ARTICLE_BODY, type=str, required=False,
                            help='Article body must be between 100 and 5000 characters if article_link is blank.')
        parser.add_argument(articles.ARTICLE_TITLE, type=str, required=False,
                            help='Title is not required. Will be replaced by body if not provided.')

        args = parser.parse_args()
        print(args.items())
        submitter_id = session['user_id']
        article_link = args[articles.ARTICLE_LINK]
        article_body = args[articles.ARTICLE_BODY]
        article_title = args[articles.ARTICLE_TITLE]

        if not article_link and not article_body:
            return {'message':
                    f"Either {articles.ARTICLE_LINK} or {articles.ARTICLE_BODY} must be provided"}, HTTPStatus.BAD_REQUEST
        if not article_link and (not article_body or len(article_body) < 100 or len(article_body) > 5000):
            return {'message':
                    "Article body must be between 100 and 5000 characters"}, HTTPStatus.BAD_REQUEST
        if not article_body:  # do scrape of link
            # article_body = articles.scrape_link(article_link) # replace with actual function
            article_body = "This is a placeholder for the scraped article body"
            if article_body is None:
                return {'message': "Failed to scrape the article body"}, HTTPStatus.BAD_REQUEST
        if article_title is None:
            article_title = article_body[:25] + "..."

        try:
            success, submission_id = articles.store_article_submission(submitter_id, article_title, article_link, article_body)
            if not success:
                return {'message': f"Failed to store the article submission {submission_id}"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {
            "message": f"Article {article_title} submitted successfully",
            "submission_id": str(submission_id),
            USER: users.get_user_if_logged_in(session),
        }, HTTPStatus.OK


@ar.route(SUBMISSIONS_EP)
class SubmittedArticles(Resource):
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized access')
    def get(self):
        """
        Get all news article links and name submitted by the logged in user.
        """
        if 'user_id' in session:
            user_id = session['user_id']
            username = users.get_user_by_id(user_id)[users.NAME]
            return {
                TYPE: DATA,
                TITLE: 'Stored Articles',
                DATA: articles.get_articles_by_username(username),
                USER: users.get_user_if_logged_in(session),
            }
        else:
            return {'message': 'No user currently logged in'}, HTTPStatus.UNAUTHORIZED


# Define the request model for bias analysis
analyze_bias_model = api.model('AnalyzeBias', {
    # 'article_id':
    # fields.String(required=True, description='ID of the article to analyze'),
    'analysis_parameters':
    fields.Raw(required=False, description='Optional parameters for analysis')
})


@ar.route(f"{ANALYSIS_EP}{ARTICLE_ID_EP}")
class AnalyzeBias(Resource):
    @api.expect(analyze_bias_model)
    @api.response(HTTPStatus.OK, 'Bias analysis completed')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid request data')
    @api.response(HTTPStatus.NOT_FOUND, 'Article not found')
    def post(self, article_id):
        """
        Analyze the bias in a submitted article.
        """
        # data = request.json
        # analysis_parameters = data.get('analysis_parameters', {})

        # Use the provided function to retrieve the article by its ID
        article = users.get_article_by_id(article_id)
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
            'analysis_result': analysis_result,
            USER: users.get_user_if_logged_in(session),
        }, HTTPStatus.OK


change_username_model = api.model('ChangeUsername', {
    'old_username': fields.String(
        required=True, description='The current username'),
    'new_username': fields.String(
        required=True, description='The new username'),
    'password': fields.String(
        required=True, description='Confirmation of the  password')
})


@us.route(UPDATE_USERNAME_EP)
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
            if users.get_user_by_name(new_username):
                return {'message': 'Username already exists.'}, HTTPStatus.BAD_REQUEST
            users.update_user_profile(old_username, password, {users.NAME: new_username})
            return {
                DATA: 'Username changed successfully.',
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.OK
        except Exception as e:
            return {
                DATA: str(e),
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.BAD_REQUEST


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


@us.route(UPDATE_PASSWORD_EP)
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
            return {DATA: 'Passwords do not match.',
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.BAD_REQUEST

        try:
            users.update_user_profile(username, old_password, {users.PASSWORD: new_password})
            return {
                DATA: 'Password changed successfully.',
                USER: users.get_user_if_logged_in(session)
                }, HTTPStatus.OK
        except Exception as e:
            return {DATA: str(e),
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.BAD_REQUEST


change_email_model = api.model('ChangeEmail', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='current password'),
    'new_email': fields.String(required=True, description='new email')
})


@us.route(UPDATE_EMAIL_EP)
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
            users.update_user_profile(username, password, {users.EMAIL: new_email})
            return {
                DATA: 'EMAIL changed successfully.',
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.OK
        except Exception as e:
            return {DATA: str(e),
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.BAD_REQUEST


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
            users.clear_data(name)
            return {
                DATA: 'Database Cleared',
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.OK
        except Exception as e:
            return {
                DATA: str(e),
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.BAD_REQUEST

    def get(self):
        """
        Get the name of every collection.
        """
        return {
            TYPE: DATA,
            TITLE: 'collection name',
            DATA: users.get_all_collection(),
            RETURN: MAIN_MENU_EP,
            USER: users.get_user_if_logged_in(session),
        }
