# userdata/user_text_data_db.py
import random
import userdata.db_connect as dbc

# Constants for field names and collection name
TEXT_CONTENT = 'text_content'
SENTIMENT_RESULT = 'sentiment_result'
UPLOAD_TIMESTAMP = 'upload_timestamp'
USER_ID = 'user_id'
TEXT_DATA_COLLECTION = 'user_text_data'

BIG_NUM = 100000000000000000000
ID_LEN = 24
MOCK_TEXT_ID = '0' * ID_LEN
MOCK_USER_ID = '0' * ID_LEN
MOCK_TEXT_CONTENT = 'Example text'
MOCK_SENTIMENT_RESULT = 'Positive'
MOCK_TIMESTAMP = '2023-11-29T12:00:00Z'

# Mock data for testing (if necessary)
mock_text_data = {
    MOCK_TEXT_ID: {
        USER_ID: MOCK_USER_ID,
        TEXT_CONTENT: MOCK_TEXT_CONTENT,
        SENTIMENT_RESULT: MOCK_SENTIMENT_RESULT,
        UPLOAD_TIMESTAMP: MOCK_TIMESTAMP
    }
}


def _gen_id() -> str:
    """
    Generates a random ID.
    """
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def store_text_upload(user_id: str, text_content: str, sentiment_result:
                      str, timestamp: str):
    """
    Stores a text upload and its sentiment analysis result in the database.
    """
    dbc.connect_db()
    text_data = {
        USER_ID: user_id,
        TEXT_CONTENT: text_content,
        SENTIMENT_RESULT: sentiment_result,
        UPLOAD_TIMESTAMP: timestamp
    }
    return dbc.insert_one(TEXT_DATA_COLLECTION, text_data)


def retrieve_user_text_uploads(user_id: str):
    """
    Retrieves all text uploads and sentiment analysis results for a given user.
    """
    dbc.connect_db()
    query = {USER_ID: user_id}
    return dbc.fetch_all(TEXT_DATA_COLLECTION, query)
