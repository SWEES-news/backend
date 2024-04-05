"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import userdata.db_connect as dbc  # userdata.

# ------ configuration for MongoDB ------ #
USER_COLLECT = 'users'
ARTICLE_COLLECTION = 'articles'
# field name for user ID in the articles collection
SUBMITTER_ID_FIELD = 'submitter_id'
ARTICLE_LINK = "article_link"
ARTICLE_TITLE = "article_title"
ARTICLE_BODY = "article_body"

# ------ DB fields ------ #
NAME = 'Username'
EMAIL = 'Email'
PASSWORD = 'Password'

# ------ DB rules ------ #
ID_LEN = 24
BIG_NUM = 100000000000000000000


def fetch_all_with_filter(collection, filt={}, projection={}, db=dbc.USER_DB):
    """
    Find with a filter and return all matching docs.
    Projection can be used to include or exclude fields.
    """
    dbc.connect_db()
    results = dbc.fetch_all_with_filter(collection, filt, projection, db)
    return results

def fetch_all_with_constrained_filter(collection, filt={}, projection={}, db=dbc.USER_DB):
    """
    Find with a filter and return all matching docs with constraints.
    Projection can be used to include or exclude fields.
    """
    dbc.connect_db()
    results = dbc.fetch_all_with_constrained_filter(collection, filt, projection, db)
    return results


def get_all_collection():
    dbc.connect_db()
    return dbc.fetch_collection_name()
