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
VECTOR_COLLECTION = 'articleEmbeddings'
# field name for user ID in the articles collection
ARTICLE_LINK = "article_link"
ARTICLE_TITLE = "article_title"
ARTICLE_BODY = "article_body"
ARTICLE_PREVIEW = "article_preview"
PRIVATE = "private"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "default"


# ------ DB fields ------ #
NAME = users.NAME
EMAIL = users.EMAIL
PASSWORD = users.PASSWORD
SUBMITTER_ID_FIELD = users.SUBMITTER_ID_FIELD
OBJECTID = '_id'
EMBEDDING_FIELD_NAME = "embedding"


def store_article_submission(submitter_id: str, article_title: str, article_link: str = "",
                             article_body: str = "", article_preview: str = "", 
                             article_embedding = "", private_article: bool = False) -> (bool, str):
    """
    Store the submitted article for review. Stores article in userDB, and embedding in vectorDB.
    """
    user = users.get_user_by_id(submitter_id)
    if not user:
        return False, f"User with {submitter_id} NOT found"

    # Create a new article submission record
    submission_record = {
        ARTICLE_LINK: article_link,
        ARTICLE_TITLE: article_title,
        ARTICLE_BODY: article_body,
        ARTICLE_PREVIEW: article_preview,
        SUBMITTER_ID_FIELD: user[OBJECTID],
        PRIVATE: private_article
    }

    dbc.connect_db()
    submission_id = dbc.insert_one(ARTICLE_COLLECTION, submission_record)

    return True, submission_id


def store_article_embedding(submitter_id: str, article_id: str, 
                             article_embedding: list[float]) -> (bool, str):
    """
    Store the submitted article for review. Stores article in userDB, and embedding in vectorDB.
    """
    user = users.get_user_by_id(submitter_id)   # ------- might remove this check ---------------
    if not user:
        return False, f"User with {submitter_id} NOT found"

    dbc.connect_db()
    vector_data = {OBJECTID: article_id, EMBEDDING_FIELD_NAME: article_embedding}
    vector_result = dbc.insert_one(VECTOR_COLLECTION, vector_data, db=dbc.VECTOR_DB)

    if vector_result is None:
        raise Exception("Issue storing article embedding in vector database.")
    return True, article_id


def get_article_by_id(article_id, user_id=None):
    """
    Fetches an article from the database by their ID.
    """
    try:
        # MUST convert the string ID to an ObjectId
        object_id = ObjectId(article_id)
    except InvalidId:
        return None

    # ret the article only if it belongs to the user or its public
    dbc.connect_db()
    article = dbc.fetch_one(ARTICLE_COLLECTION, {OBJECTID: object_id})
    if article and (article[SUBMITTER_ID_FIELD] == user_id or article[PRIVATE] == "False"):
        return article
    else:
        return None


def get_article_and_embedding_by_id(article_id, user_id=None):
    """
    Fetches an article and its embedding from the database.
    """
    try:
        # MUST convert the string ID to an ObjectId
        object_id = ObjectId(article_id)
    except InvalidId:
        return None

    dbc.connect_db()
    filter = {OBJECTID: object_id}
    article = dbc.fetch_one(ARTICLE_COLLECTION, filter)

    # to ret the article only if it belongs to the user or its public:
    # ...and (article[SUBMITTER_ID_FIELD] == user_id or article[PRIVATE] == "False")
    if article:
        vector = dbc.fetch_one(VECTOR_COLLECTION, filter, db=dbc.VECTOR_DB)
        return article, vector
    else:
        return None


def fetch_all_with_filter(filt={}, projection={}, constrained=False, title_keyword=None, submitter_id=None):
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
        articles = extras.fetch_all_with_constrained_filter(ARTICLE_COLLECTION, filt, projection)
    else:
        articles = extras.fetch_all_with_filter(ARTICLE_COLLECTION, filt, projection)
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


def fetch_with_combined_filter(or_filter, and_filter, remove_filter, title_keyword=None, db=dbc.USER_DB):
    """
    Find with a filter and return all matching docs.
    Combines OR and AND filters, with projection to remove certain fields.
    """
    if title_keyword:
        query_or_filter = {ARTICLE_TITLE: {'$regex': re.compile(title_keyword, re.IGNORECASE)}, **or_filter}
    else:
        query_or_filter = or_filter
    articles = extras.fetch_with_combined_filter(ARTICLE_COLLECTION, query_or_filter, and_filter, remove_filter, db)
    return articles
