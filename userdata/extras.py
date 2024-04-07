"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import userdata.db_connect as dbc  # userdata.

from bson.objectid import ObjectId
from bson.errors import InvalidId

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


def fetch_with_combined_filter(collection, or_filter, and_filter, remove_filter, db=dbc.USER_DB):
    """
    Find with a filter and return all matching docs.
    Combines OR and AND filters, with projection to remove certain fields.
    """
    # Combine OR and AND conditions
    query_conditions = []

    # Add OR conditions
    if or_filter:
        or_conditions = [{'$or': [{key: value} for key, value in or_filter.items()]}]
        query_conditions.extend(or_conditions)

    # Add AND conditions
    if and_filter:
        and_conditions = [{key: value} for key, value in and_filter.items()]
        query_conditions.extend(and_conditions)

    # Construct final query
    query = {'$and': query_conditions} if query_conditions else {}

    # Connect to the database
    dbc.connect_db()
    return dbc.fetch_all_with_filter(collection, query, projection=remove_filter, db=db)


def str_to_objectid(str_id):
    """
    Convert a string ID to an ObjectId.
    """
    if not isinstance(str_id, (str, bytes, ObjectId)):
        raise TypeError(f"Expected id to be str or bytes, got {type(str_id)}")

    try:
        # MUST convert the string ID to an ObjectId
        object_id = ObjectId(str_id)
    except InvalidId:
        return None
    return object_id
