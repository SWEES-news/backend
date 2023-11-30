import pytest
import userdata.user_text_data_db as text_data

@pytest.fixture(scope='function')
def mock_text_upload():
    user_id = 'mock_user_id'
    text_content = 'Example text content'
    sentiment_result = 'Positive'
    timestamp = '2023-11-29T12:00:00Z'
    text_id = text_data.store_text_upload(user_id, text_content, sentiment_result, timestamp)
    yield user_id, text_id, text_content, sentiment_result, timestamp
    # Mock cleanup (if necessary)
    del text_data.mock_text_data[text_id]

def test_store_text_upload(mock_text_upload):
    user_id, text_id, text_content, sentiment_result, timestamp = mock_text_upload
    assert isinstance(text_id, str)
    assert text_data.mock_text_data[text_id][text_data.USER_ID] == user_id
    assert text_data.mock_text_data[text_id][text_data.TEXT_CONTENT] == text_content
    assert text_data.mock_text_data[text_id][text_data.SENTIMENT_RESULT] == sentiment_result
    assert text_data.mock_text_data[text_id][text_data.UPLOAD_TIMESTAMP] == timestamp

def test_retrieve_user_text_uploads(mock_text_upload):
    user_id, text_id, _, _, _ = mock_text_upload
    uploads = text_data.retrieve_user_text_uploads(user_id)
    assert isinstance(uploads, list)
    assert any(upload for upload in uploads if upload[text_data.USER_ID] == user_id and text_id in text_data.mock_text_data)
