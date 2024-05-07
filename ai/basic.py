import os
from dotenv import load_dotenv

import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# from langchain_openai import OpenAIEmbeddings
from langchain_openai.embeddings.base import OpenAIEmbeddings

import os
import sys
import inspect

# Modifying sys.path to include parent directory for local imports
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import userdata.db_connect as dbc
import userdata.articles as articles
DB_NAME = dbc.VECTOR_DB
COLLECTION_NAME = articles.ARTICLE_COLLECTION
ATLAS_VECTOR_SEARCH_INDEX_NAME = articles.ATLAS_VECTOR_SEARCH_INDEX_NAME
EMBEDDING_FIELD_NAME = articles.EMBEDDING_FIELD_NAME

load_dotenv()

MODEL = 'gpt-4-turbo-preview'  # 128,000 token max
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding_generator = None


PROMPT_TEMPLATE = (
    'Hello! You are a bias-finding analyst who has been tasked with '
    'determining the biases of a given news article. Please provide insights '
    'on this article while keeping in mind types of bias that may be '
    'apparent:\n'
    # see bias-analysis.md
    ' - Selection Bias: This occurs when a news outlet selectively reports on '
    'certain events over others, which can shape public perception by '
    'highlighting some issues while ignoring others.\n'
    ' - Reporting Bias: It involves a partial presentation of facts, where '
    'some details are emphasized over others to support a specific viewpoint. '
    'This can also include the omission of key facts that might contradict '
    'the outlet\'s preferred narrative.\n'
    ' - Confirmation Bias: This is more about the audience than the news '
    'outlet, where people favor information that confirms their preexisting '
    'beliefs. However, media outlets can exploit this bias by catering '
    'content to what they believe their audience wants to see or hear.\n'
    ' - Bias by Headline: Sometimes headlines can be misleading or designed '
    'to elicit an emotional response, rather than accurately summarizing the '
    'content of the article.\n'
    ' - Bias by Placement: The prominence given to a story, such as '
    'front-page news versus a brief mention in the back, can indicate the '
    'outlet\'s priorities or biases.\n'
    ' - Source Bias: This refers to the reliance on sources that may have a '
    'vested interest in how the story is told. It\'s important to consider '
    'who is being quoted and why.\n'
    ' - Visual Bias: Images, videos, and even the layout of a story can '
    'influence how the information is perceived. Visual elements can be used '
    'to evoke emotions or subtly sway opinion.\n'
    ' - Language and Tone Bias: The choice of words, the tone of the '
    'article, and the use of loaded language can all reveal bias. Neutral '
    'reporting strives for objective language devoid of any insinuation or '
    'judgment.\n\n'

    # TODO in future: retrieve additional articles based on
    # ...their analyses and similarity to the input text
    'Context from related articles is provided below:\n\n'
    '"""{context}"""\n\n'

    'Here is the news article to analyze, delimited by triple quotes ("""):'
    '\n\n"""{content}"""\n\n'
    'Your response:\n'
)


def generate_embedding(text):
    if not embedding_generator:
        embedding_generator = OpenAIEmbeddings(disallowed_special=(), 
                                openai_api_key=OPENAI_API_KEY, 
                                model="text-embedding-3-small",
                                dimensions=1536)  # model="text-embedding-3-large"
    try:
        embedding = embedding_generator.embed_query(text)
        return embedding
    except Exception as e:
        print(f"An error occurred while generating an embedding: {e}")
        return None


def perform_vector_search(query_embedding, k=3):
    """
    Perform a vector similarity search to find the top 'k' similar articles based on the embedding.
    
    Args:
        query_embedding (list of float): The embedding vector of the query.
        k (int): The number of similar articles to retrieve.

    Returns:
        list of ObjectIds: A list of ObjectIds for the top 'k' similar articles.
    """
    try:
        dbc.connect_db()
        vector_db = dbc.client_vector[dbc.VECTOR_DB]
        vector_collection = vector_db[articles.VECTOR_COLLECTION]

        # Construct the search query using MongoDB Atlas's vector search capabilities
        search_query = {
            "$vectorSearch": {
                "index": articles.ATLAS_VECTOR_SEARCH_INDEX_NAME,
                "path": articles.EMBEDDING_FIELD_NAME,
                "queryVector": query_embedding,
                "numCandidates": 100,  # Recommended to be higher than 'k' for accuracy
                "limit": k
            }
        }

        # Execute the search and retrieve the document IDs
        results = vector_collection.aggregate([
            search_query,
            {"$project": {articles.OBJECTID: 1}}  # Only return the _id field of the documents
        ])

        # Extract the IDs from the results
        article_ids = [result[articles.OBJECTID] for result in results]
        print(f'{article_ids=}')
        return article_ids

    except Exception as e:
        logging.error(f"Error during vector search: {str(e)}")
        return []


def analyze_content(article_text: str, article_embedding: list[float] = None):
    """
    Analyzes the article text for bias using related articles as context.
    """
    try:
        # might remove this, existing articles in DB should already have embedding ---
        if not article_embedding:
            article_embedding = generate_embedding(article_text)
        
        # Perform vector search to find + retrieve similar articles
        similar_article_ids = perform_vector_search(article_embedding, k=3)
        similar_articles = articles.get_context_articles_by_ids(similar_article_ids)
        similar_articles_texts = [art[articles.ARTICLE_BODY] for art in similar_articles if art is not None]
        
        # Prepare the context by combining the content of similar articles
        if similar_articles_texts:
            context = " ".join(similar_articles_texts)
        else:
            context = ""
        
        # Prepare the prompt with the original article and the context
        formatted_prompt = PROMPT_TEMPLATE.format(content=article_text, context=context)
        prompt = ChatPromptTemplate.from_template(formatted_prompt)
        
        # Set up the OpenAI API call
        model = ChatOpenAI(model=MODEL, openai_api_key=OPENAI_API_KEY)
        chain = prompt | model | StrOutputParser()
        
        # Execute the analysis
        response = chain.invoke({"content": article_text})
        return response
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None


def read_content(file_path: str) -> str:
    """Reads content from a file and returns the content as a string.
    Returns None if there's an error reading the file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError as e:
        logging.error(f"File not found {file_path}: {e}")
    except IOError as e:
        logging.error(f"IO error reading {file_path}: {e}")
    return None


def write_response(file_path: str, response: str):
    """Writes a response to a file."""
    try:
        with open(file_path, 'w') as file:
            print(response, file=file)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")


def main():
    content_file = 'ai/test_article_2.txt'
    response_file = 'ai/test_response_2.md'
    
    content = read_content(content_file)
    embedding = generate_embedding(content)

    # # update DB
    # submitterID = 'existing id'
    # success, mongoID = articles.store_article_submission(submitterID, 
    #     "Mercedes-Benz Walks Back", article_body=content)
    # if success:
    #     print("Successfully stored article!")
    #     success, _ = articles.store_article_embedding(submitterID, mongoID, embedding)
    #     print("Successfully stored article embedding!")
    #     print(embedding[:4])


    response = analyze_content(content, embedding)
    write_response(response_file, response)
    print(response[:75])


if __name__ == "__main__":
    main()
