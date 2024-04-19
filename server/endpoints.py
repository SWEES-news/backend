"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from flask import Flask, request, session
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS
from http import HTTPStatus
import werkzeug.exceptions as wz
import userdata.extras as extras

import os
import sys
import inspect
import userdata.users as users
import userdata.articles as articles
import string
import examples.form as ff

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
col = api.namespace('collections', description="generic operations for data in collections")
# ns = api.Namespace('basic stuff', description="this is basic stuff")
# use ns.route instead of api.route

# ------ Namespace names ------ #
USERS_EP = f'/{us.name}'
ARTICLES_EP = f'/{ar.name}'
COLLECTIONS_EP = f'/{col.name}'

# ------ Endpoint names ------ #
ACCOUNT_EP = '/account'
REGISTER_EP = '/register'
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
UPDATE_USERNAME_EP = '/update/username'
UPDATE_PASSWORD_EP = '/update/password'
UPDATE_EMAIL_EP = '/update/email'
DELETE_EP = '/update/delete'
STATUS_EP = '/status'
SUBMIT_EP = '/submit'
SUBMISSIONS_EP = '/submissions'
ANALYSIS_EP = '/submissions/analysis'
ENDPOINTS_EP = '/endpoints'
ALL_EP = '/all'
SURVEY_EP = '/survey'

MAIN_MENU_EP = '/MainMenu'
CLEAR_EP = '/clear'
USER_NAME_EP = '/<string:name>'
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

punctuation_chars = string.punctuation


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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def get(self):
        """
        Get a list of all users. DEBUG REMOVE FROM PROD.
        """
        user_id = session.get('user_id', None)
        print(session)
        if not user_id:
            return {DATA: 'No user currently logged in.'}, HTTPStatus.UNAUTHORIZED

        if not users.has_admin_privilege(user_id):
            return {DATA: 'You are not authorized to clear the database.'}, HTTPStatus.UNAUTHORIZED

        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: users.get_users(),
            RETURN: MAIN_MENU_EP,
        }, HTTPStatus.OK


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
            return {DATA: 'No user currently logged in'}, HTTPStatus.UNAUTHORIZED


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
            if users.verify_user_by_name(username, password):
                user_id = users.get_user_by_name(username)[users.OBJECTID]
                session['user_id'] = user_id
                data = users.get_user_if_logged_in(session)
                if data is None:
                    raise wz.NotFound('Problem with login')
                return {
                    DATA: 'Login successful',
                    USER: data,
                    }, HTTPStatus.OK
            else:
                raise wz.Unauthorized('Falled to login')
        except (ValueError, KeyError) as e:
            print(str(e))
            raise wz.BadRequest(f'{str(e)} Something Went Really Wrong')


@us.route(LOGOUT_EP)
class UserLogout(Resource):
    @api.response(HTTPStatus.OK, 'Successful login')
    @api.response(HTTPStatus.BAD_REQUEST, 'Something went wrong')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Wrong password')
    def get(self):
        try:
            if 'user_id' in session:
                userid = session['user_id']
                session.pop('user_id')
                username = users.get_user_by_id(userid)[users.NAME]
                return {DATA: f'Logged out {username}'}, HTTPStatus.OK
            else:
                msg = 'No user currently logged in'
                print(msg)
                return {DATA: msg}, HTTPStatus.BAD_REUNAUTHORIZEDQUEST
        except Exception as e:
            return {DATA: str(e)}, HTTPStatus.BAD_REQUEST


@us.route(STATUS_EP)
class LoggedIn(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    def get(self):
        """
        Check if a user is currently logged in.
        """
        if 'user_id' in session:
            print(session)
            return {
                DATA: 'User is currently logged in.',
                USER: users.get_user_if_logged_in(session)
                }, HTTPStatus.OK
        else:
            return {
                DATA: 'No user currently logged in.',
                USER: 'None'
                }, HTTPStatus.UNAUTHORIZED


article_query_parser = reqparse.RequestParser()
article_query_parser.add_argument('title_keyword', type=str, required=False, help='Keyword to search in article titles')


@ar.route(ALL_EP)
class Articles(Resource):
    """
    Gets all public articles that have been submitted to the site by all users
    Option to filter by title keyword
    """
    @api.expect(article_query_parser)
    def get(self):
        """
        Get all news article links and titles.
        """
        article_query_parser.parse_args()
        title_keyword = request.args.get('title_keyword', None)
        return {
            TYPE: DATA,
            TITLE: 'Stored Articles',
            DATA: articles.fetch_with_combined_filter(
                and_filter={articles.PRIVATE: 'False'},
                or_filter={},
                remove_filter={articles.ARTICLE_BODY: 0, articles.SUBMITTER_ID_FIELD: 0},
                title_keyword=title_keyword
                ),
            RETURN: MAIN_MENU_EP,
        }


@ar.route(SUBMISSIONS_EP)
class SubmittedArticles(Resource):
    @api.response(HTTPStatus.OK, 'Article submitted successfully')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized access')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid request')
    @api.expect(article_query_parser)
    def get(self):
        """
        Get all news article links and name submitted by the logged in user.
        """
        try:
            if 'user_id' in session:
                user_id = session['user_id']
                article_query_parser.parse_args()
                title_keyword = request.args.get('title_keyword', None)
                return {
                    TYPE: DATA,
                    TITLE: 'Stored Articles',
                    DATA: articles.fetch_with_combined_filter(
                        and_filter={articles.SUBMITTER_ID_FIELD: user_id},
                        or_filter={},
                        remove_filter={articles.ARTICLE_BODY: 0, articles.SUBMITTER_ID_FIELD: 0},
                        title_keyword=title_keyword
                    ),
                    USER: users.get_user_if_logged_in(session),
                }
            else:
                return {DATA: 'No user currently logged in'}, HTTPStatus.UNAUTHORIZED
        except Exception as e:
            return {DATA: str(e)}, HTTPStatus.BAD_REQUEST


@ar.route('/<string:article_id>')
@api.doc(params={'article_id': 'An ID of an article'})
class ArticleById(Resource):
    @api.response(HTTPStatus.OK, 'Article submitted successfully')
    @ar.response(HTTPStatus.NOT_FOUND, 'Article not found')
    @ar.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized access')
    def get(self, article_id):
        """
        Get an article by its ID
        """
        user_id = session.get('user_id', None)
        if not user_id:
            # return {DATA: 'No user currently logged in'}, HTTPStatus.UNAUTHORIZED
            pass  # lets say they can still view public ones

        article = articles.get_article_by_id(article_id, user_id)  # does the auth stuff
        if article:
            return article
        else:
            return {DATA: 'Article not found or not authorized'}, HTTPStatus.NOT_FOUND


submit_article_model = api.model('SubmitArticle', {
    articles.ARTICLE_LINK: fields.String(description='Link to the article'),
    articles.ARTICLE_BODY: fields.String(description='Body of the article'),
    articles.ARTICLE_TITLE: fields.String(required=True, description='Title of the article'),
    articles.PRIVATE: fields.String(description='Is the article/text private?'),
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
        parser.add_argument(articles.PRIVATE, type=str, required=False,
                            help='Is the article private?')

        args = parser.parse_args()
        print(args.items())
        submitter_id = session['user_id']
        article_link = args[articles.ARTICLE_LINK]
        article_body = args[articles.ARTICLE_BODY]
        article_title = args[articles.ARTICLE_TITLE]
        # print(args[articles.PRIVATE])
        private_article = args[articles.PRIVATE] or False

        if not article_link and not article_body:
            return {DATA:
                    f"Either {articles.ARTICLE_LINK} or {articles.ARTICLE_BODY} must be provided"}, HTTPStatus.BAD_REQUEST
        if not article_link and (not article_body or len(article_body) < 100 or len(article_body) > 5000):
            return {DATA:
                    "Article body must be between 100 and 5000 characters"}, HTTPStatus.BAD_REQUEST
        if not article_body:  # do scrape of link
            # article_body = articles.scrape_link(article_link) # replace with actual function
            article_body = "This is a placeholder for the scraped article body"
            if article_body is None:
                return {DATA: "Failed to scrape the article body"}, HTTPStatus.BAD_REQUEST
        if article_title == "":
            article_title = article_body[:25].strip().strip(punctuation_chars) + "..."

        article_preview = article_body[:150].strip().strip(punctuation_chars) + "..."

        try:
            success, submission_id = articles.store_article_submission(submitter_id, article_title, article_link,
                                                                       article_body, article_preview, private_article)
            if not success:
                return {DATA: f"Failed to store the article submission {submission_id}"}, HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {DATA: str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {
            "message": f"Article {article_title} submitted successfully",
            "submission_id": str(submission_id),
            USER: users.get_user_if_logged_in(session),
        }, HTTPStatus.OK


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
        article = users.get_article_by_id(article_id)  # this needs to be secure and use user_id MUST
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def put(self):
        """
        Update the username of a user.
        """
        try:
            user_id = session.get('user_id', None)
            if not user_id:
                return {DATA: 'No user currently logged in.'}, HTTPStatus.UNAUTHORIZED

            response = request.json
            new_username = response.get(users.NAME)
            password = response.get(users.PASSWORD)

            try:
                if users.get_user_by_name(new_username):
                    return {DATA: 'Username already exists.'}, HTTPStatus.BAD_REQUEST
                user_id_object = extras.str_to_objectid(user_id)
                users.update_user_profile(user_id_object, password, {users.NAME: new_username})
                return {
                    DATA: 'Username changed successfully.',
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.OK
            except Exception as e:
                return {
                    DATA: str(e),
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.BAD_REQUEST

        except Exception as e:
            return {DATA: str(e),
                    }, HTTPStatus.BAD_REQUEST


change_password_model = api.model('ChangePassword', {
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def put(self):
        """
        Update the password of a user.
        """
        user_id = session.get('user_id', None)
        if not user_id:
            return {DATA: 'No user currently logged in.',
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.UNAUTHORIZED

        response = request.json
        old_password = response.get('old_password')
        new_password = response.get('new_password')
        confirm_new_password = response.get('confirm_new_password')

        if new_password != confirm_new_password:
            return {DATA: 'New passwords do not match.',
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.BAD_REQUEST

        try:
            user_object_id = extras.str_to_objectid(user_id)
            users.update_user_profile(user_object_id, old_password, {users.PASSWORD: new_password})
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def put(self):
        """
        Update the email of a user.
        """
        user_id = session.get('user_id', None)
        if not user_id:
            return {DATA: 'No user currently logged in.',
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.UNAUTHORIZED

        response = request.json
        password = response.get(users.PASSWORD)
        new_email = response.get(users.EMAIL)

        try:
            user_object_id = extras.str_to_objectid(user_id)
            users.update_user_profile(user_object_id, password, {users.EMAIL: new_email})
            return {
                DATA: 'EMAIL changed successfully.',
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.OK
        except Exception as e:
            return {DATA: str(e),
                    USER: users.get_user_if_logged_in(session),
                    }, HTTPStatus.BAD_REQUEST


password_model = api.model('PasswordModel', {
    users.PASSWORD: fields.String(required=True, description='User password')
})


@us.route(DELETE_EP)
class RemoveUser(Resource):
    @api.expect(password_model)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def delete(self):
        """
        Remove/delete a user.
        """
        user_id = session.get('user_id', None)
        password = request.json.get(users.PASSWORD)
        if user_id:
            try:
                object_id = extras.str_to_objectid(user_id)
                if users.verify_user(object_id, password):
                    users.del_user_by_id(object_id)
                    session.pop('user_id')
                else:
                    raise ValueError()
            except KeyError:
                raise wz.NotFound('User not found.')
            except ValueError:
                raise wz.Unauthorized('Password incorrect.')

            return {DATA: 'User removed successfully.'}
        raise wz.Unauthorized('No user logged in.')


DatabaseClear = api.model('Database Name', {
    'Name': fields.String(required=True, description='Database'),
})


@col.route('/db')
class Collection(Resource):
    @api.expect(DatabaseClear)
    def delete(self):
        """
        Clears the specified Database.
        """
        user_id = session.get('user_id', None)
        if not user_id:
            return {DATA: 'No user currently logged in.'}, HTTPStatus.UNAUTHORIZED

        if not users.has_admin_privilege(user_id):
            return {DATA: 'You are not authorized to clear the database.'}, HTTPStatus.UNAUTHORIZED

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


@col.route(f"{CLEAR_EP}/users")
class UsersCollectionWipe(Resource):
    def delete(self):
        """
        Clears the users Database.
        """
        user_id = session.get('user_id', None)
        if not user_id:
            return {DATA: 'No user currently logged in.'}, HTTPStatus.UNAUTHORIZED

        if not users.has_admin_privilege(user_id):
            return {DATA: 'You are not authorized to clear the database.'}, HTTPStatus.UNAUTHORIZED

        try:
            data = users.clear_data('users')
            return {
                DATA: 'Users Database Cleared: ' + data,
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.OK
        except Exception as e:
            return {
                DATA: str(e),
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.BAD_REQUEST


@col.route(f"{CLEAR_EP}/articles")
class ArticlesCollectionWipe(Resource):
    def delete(self):
        """
        Clears the articles Database.
        """
        user_id = session.get('user_id', None)
        if not user_id:
            return {DATA: 'No user currently logged in.'}, HTTPStatus.UNAUTHORIZED

        if not users.has_admin_privilege(user_id):
            return {DATA: 'You are not authorized to clear the database.'}, HTTPStatus.UNAUTHORIZED

        try:
            users.clear_data('articles')
            return {
                DATA: 'articles Database Cleared',
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.OK
        except Exception as e:
            return {
                DATA: str(e),
                USER: users.get_user_if_logged_in(session),
                }, HTTPStatus.BAD_REQUEST


@us.route(SURVEY_EP)
class UserSurvey(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.doc(param=ff.get_form())
    def get(self):
        # args = request.json.get()
        return ff.get_form(), HTTPStatus.OK
