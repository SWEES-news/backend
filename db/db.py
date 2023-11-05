"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

NAME = 'username'
PASSWORD = 'password'
EMAIL = 'email'


def get_sample_user():
    return {NAME: '1', PASSWORD: '1', EMAIL: '1@gmail.com'}


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}

# future use
# def init_app(app):
#     db.init_app(app)
#     Migrate(app, db)
#     return True
