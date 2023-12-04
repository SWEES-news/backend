"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields

import werkzeug.exceptions as wz

import userdata.db as data
import userdata.newsdb as news
# from http import HTTPStatus


app = Flask(__name__)

api = Api(app)

MENU = 'menu'
NUM = 0
MAIN_MENU = 'MainMenu'
MAIN_MENU_EP = '/MainMenu'
MAIN_MENU_NM = "Welcome to our site!"
USERS = 'users'
HELLO_STR = 'hello'
HELLO_SLASH = '/hello'
USERS_SLASH = '/users'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'
USER_ID = 'UserID'
NEWS_LINK = 'NewsPage'
NEWS_LINK_SLASH = '/news'
NEWS_ID = 'NewsID'


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


@api.route(f'/{MAIN_MENU}')
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
    data.NAME: fields.String,
    data.EMAIL: fields.String,
    data.PASSWORD: fields.Integer,
})


@api.route(f'{USERS_SLASH}')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: data.get_users(),
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(user_model)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user.
        """
        name = request.json[data.NAME]
        password = request.json[data.EMAIL]
        email = request.json[data.EMAIL]

        try:
            new_id = data.add_user(email, name, password)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {USER_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route('/user/<int:user_id>')
class UserDetail(Resource):
    """
    This class supports fetching details of a specific user.
    """
    def get(self, user_id):
        """
        This method returns details of a specific user.
        """
        user = data.get_user_by_id(user_id)
        if user:
            return user
        else:
            api.abort(HTTPStatus.NOT_FOUND, f'User {user_id} not found')


news_model = api.model('NewArticle', {
    news.NAME: fields.String,
    news.LINK: fields.Integer,
})


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
            new_id = news.add_user(name, link)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {NEWS_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

@api.route('/submit-article')
class SubmitArticle(Resource):
    @api.expect(submit_article_model)
    @api.response(HTTPStatus.OK, 'Article submitted successfully')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid data')
    def post(self):
        """
        Submit an article for review.
        """
        data = request.json
        article_link = data['article_link']
        submitter_id = data['submitter_id']
        
        # Validate the input data
        if not article_link or not submitter_id:
            api.abort(HTTPStatus.BAD_REQUEST, "Invalid data: 'article_link' and 'submitter_id' are required.")

        # Implement logic to store the article submission for review.
        # For example, you might save it to a database.
        submission_id = store_article_submission(article_link, submitter_id)

        return {"message": "Article submitted successfully", "submission_id": submission_id}, HTTPStatus.OK

submit_article_model = api.model('SubmitArticle', {
    'article_link': fields.String(required=True, description='The URL link to the article'),
    'submitter_id': fields.String(required=True, description='The ID of the user submitting the article')
})