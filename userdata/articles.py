"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import userdata.db_connect as dbc  # userdata.
from bson.objectid import ObjectId
from bson.errors import InvalidId
import userdata.extras as extras
import userdata.users as users  # articles depends on user, avoid circular import!
import re


# ------ configuration for MongoDB ------ #
USER_COLLECT = 'users'
ARTICLE_COLLECTION = 'articles'
# field name for user ID in the articles collection
ARTICLE_LINK = "article_link"
ARTICLE_TITLE = "article_title"
ARTICLE_BODY = "article_body"
PRIVATE = "private"


# ------ DB fields ------ #
NAME = users.NAME
EMAIL = users.EMAIL
PASSWORD = users.PASSWORD
SUBMITTER_ID_FIELD = users.SUBMITTER_ID_FIELD
OBJECTID = '_id'


def store_article_submission(submitter_id: str, article_title: str, article_link: str = "",
                             article_body: str = "", private_article: bool = False) -> (bool, str):
    """
    Store the submitted article for review.
    """
    user = users.get_user_by_id(submitter_id)
    if not user:
        return False, f"User with {submitter_id} NOT found"

    # Create a new article submission record
    submission_record = {
        ARTICLE_LINK: article_link,
        ARTICLE_TITLE: article_title,
        ARTICLE_BODY: article_body,
        SUBMITTER_ID_FIELD: user[OBJECTID],
        PRIVATE: private_article
    }

    dbc.connect_db()
    submission_id = dbc.insert_one(ARTICLE_COLLECTION, submission_record)
    return True, submission_id


def get_article_by_id(article_id):
    """
    Fetches an article from the database by their ID.
    """
    try:
        # MUST convert the string ID to an ObjectId
        object_id = ObjectId(article_id)
    except InvalidId:
        return None

    dbc.connect_db()
    return dbc.fetch_one(ARTICLE_COLLECTION, {OBJECTID: object_id})


def fetch_all_with_filter(filt={}, constrained=False, title_keyword=None, submitter_id=None):
    """
    Find with a filter and return all matching docs.
    If a title_keyword is provided, it filters articles by titles containing that keyword.
    """
    # Connect to the database (if not already connected)
    if title_keyword:
        # Use regular expressions for case-insensitive search
        filt[ARTICLE_TITLE] = {'$regex': re.compile(title_keyword, re.IGNORECASE)}

    if submitter_id:
        filt[SUBMITTER_ID_FIELD] = submitter_id

    if constrained:
        articles = extras.fetch_all_with_constrained_filter(ARTICLE_COLLECTION, filt)
    else:
        articles = extras.fetch_all_with_filter(ARTICLE_COLLECTION, filt)
    return articles


def fetch_all():
    """
    Find all.
    """
    # Connect to the database (if not already connected)
    articles = fetch_all_with_filter()
    return articles


def get_articles_by_username(username):
    """
    Fetch all articles submitted by a specific user identified by username.

    :param username: The username of the user.
    :return: A list of articles submitted by the user.
    """
    user = users.get_user_by_name(username)
    if not user:
        return f"User {username} NOT found"  # User not found

    user_id = user[OBJECTID]

    # Fetch all articles submitted by this user
    articles = fetch_all_with_filter({SUBMITTER_ID_FIELD: user_id})
    return articles
