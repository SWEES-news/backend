import os
import sys
import logging
from newsdataapi import NewsDataApiClient

# Set up logging
logging.basicConfig(filename='newsdataapi_client.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Get the API key from the environment variable
api_key = os.environ.get('NEWS_API_KEY')
if api_key is None:
    logging.error("API key not found in environment variables")
    print("Please set the NEWS_API_KEY environment variable. Check README for instructions.")
    sys.exit(1)

api = NewsDataApiClient(apikey=api_key)

# Define a function to fetch news based on query parameters
def fetch_news(query_params):
    try:
        response = api.news_api(**query_params)
        if response['status'] == 'success':
            logging.info("News fetched successfully.")
            return response
        else:
            logging.error("Error fetching news: " + str(response))
            return None
    except Exception as e:
        logging.error("Exception occurred: " + str(e))
        return None

def main():
    # Example usage: pass query parameters received from command line or default ones
    query_params = {
        'q': 'python',
        'language': 'en',
        # Add other parameters as needed
    }
    news_response = fetch_news(query_params)
    if news_response:
        # Process and print the news response here
        print(news_response)

if __name__ == '__main__':
    main()
