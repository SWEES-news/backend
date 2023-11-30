import random

# Constants for field names and collection name
TEXT_CONTENT = 'text_content'
SENTIMENT_RESULT = 'sentiment_result'
UPLOAD_TIMESTAMP = 'upload_timestamp'
USER_ID = 'user_id'
TEXT_DATA_COLLECTION = 'user_text_data'

BIG_NUM = 100000000000000000000
ID_LEN = 24


mock_text_data = {}


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def store_text_upload(user_id: str, text: str, sentiment: str, timestamp: str):
    text_id = _gen_id()
    mock_text_data[text_id] = {
        USER_ID: user_id,
        TEXT_CONTENT: text,
        SENTIMENT_RESULT: sentiment,
        UPLOAD_TIMESTAMP: timestamp
    }
    return text_id


def retrieve_user_text_uploads(user_id: str):
    return [data for _, data in mock_text_data.items()
            if data[USER_ID] == user_id]
