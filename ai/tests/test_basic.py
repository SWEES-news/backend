import os
import sys
import inspect
import tempfile
import pytest
from unittest.mock import patch

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from basic import analyze_content, read_content, write_response

@pytest.fixture
def sample_texts():
    return ["Sample news article 1", "Sample news article 2"]

def test_analyze_content(sample_texts):
    # Mocking the LangChain pipeline
    with patch('basic.ChatPromptTemplate.from_template') as mock_prompt_template, \
         patch('basic.ChatOpenAI') as mock_chat_openai, \
         patch('basic.StrOutputParser') as mock_output_parser:

        # Mocking the chain response
        mock_output_parser.return_value = ["Analysis 1", "Analysis 2"]

        # Call the function
        responses = analyze_content(sample_texts)

        # Assert the correct calls to LangChain components
        mock_prompt_template.assert_called_once()
        mock_chat_openai.assert_called_once_with(model='gpt-4-turbo-preview')
        mock_output_parser.assert_called_once()

        # Assert the correct response
        assert responses == ["Analysis 1", "Analysis 2"]
