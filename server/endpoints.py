"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api
from db import db, migrate  # only import db and migrate
from db.models import User  # import User model
from db.schemas import UserSchema, ma  # import schemas and ma


app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)

api = Api(app)


MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to our site!"
USERS = 'users'
HELLO_STR = 'hello'
HELLO_SLASH = '/hello'


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


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.route(f'/{USERS}')
class Users(Resource):
    """
    This class supports fetching a list of all users and adding a new user.
    """
    def get(self):
        """
        This method returns all users.
        """
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        """
        This method adds a new user.
        """
        data = api.payload
        if not data:
            return {"message": "No input data provided"}, 400
        # Validate data
        try:
            validData = user_schema.load(data)
        except Exception as e:
            return {"message": str(e)}, 400

        # Check for existing user by username or email
        existing_user = User.query.filter(
            (User.username == data['username']) | (User.email == data['email'])
        ).first()
        if existing_user:
            return {"message": "Username or email already exists"}, 400

        # Create and add new user to db
        new_user = User(
            username=validData['username'],
            email=validData['email'],
            password=validData['password']  # hash this
        )
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 201
