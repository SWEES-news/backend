import userdata.db_connect as dbc
# from datetime import datetime
import userdata.extras as extras
from bson.objectid import ObjectId
from bson.errors import InvalidId

# Constants
COMMENT_COLLECTION = 'comments'
ARTICLE_ID_FIELD = 'article_id'
USER_ID_FIELD = 'user_id'
TEXT_FIELD = 'text'
PARENT_ID_FIELD = 'parent_id'
TIMESTAMP_FIELD = 'timestamp'
OBJECTID = "_id"


def post_comment(article_id, user_id, text, parent_id=None):
    """
    Post a new comment or reply to an article. Assumes all user checks are performed upstream.
    Validates and sanitizes input to avoid XSS and check for profanity.
    """
    sanitized_text = extras.sanitize_text(text)

    comment = {
        ARTICLE_ID_FIELD: article_id,
        USER_ID_FIELD: user_id,
        TEXT_FIELD: sanitized_text,
        PARENT_ID_FIELD: parent_id,
        # TIMESTAMP_FIELD: datetime.utcnow()
    }
    inserted_id = dbc.insert_one(COMMENT_COLLECTION, comment)
    return inserted_id


def get_comments_by_article(article_id):
    """
    Retrieve all comments for a given article.
    """
    filt = {ARTICLE_ID_FIELD: article_id}
    comments = dbc.fetch_all_with_filter(COMMENT_COLLECTION, filt)
    return comments


def get_reply_comments(parent_id):
    """
    Retrieve all replies to a specific comment.
    """
    filt = {PARENT_ID_FIELD: parent_id}
    replies = dbc.fetch_all_with_filter(COMMENT_COLLECTION, filt)
    return replies


def delete_comment(comment_id, user_id):
    """
    Allow a user to delete their own comment. Validates user ownership.
    This function safely handles invalid ID formats and authorization.
    """
    try:
        object_id = ObjectId(comment_id)
    except InvalidId:
        raise ValueError("Invalid comment ID format")

    comment = dbc.fetch_one(COMMENT_COLLECTION, {OBJECTID: object_id})
    if not comment:
        raise Exception("Comment not found")

    if comment[USER_ID_FIELD] != user_id:
        raise PermissionError("Unauthorized to delete this comment")

    result = dbc.del_one(COMMENT_COLLECTION, {OBJECTID: object_id})
    if result.deleted_count == 0:
        raise Exception("Failed to delete the comment")
    return True
