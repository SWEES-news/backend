from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

db = SQLAlchemy()


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}


def init_app(app):
    db.init_app(app)
    Migrate(app, db)
    return True
