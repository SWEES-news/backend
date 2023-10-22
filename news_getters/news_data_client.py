# *** API Credits  200/day *** 
# howto: https://newsdata.io/blog/news-api-python-client/
from newsdataapi import NewsDataApiClient
import os

# Get the API key from the environment variable
api_key = os.environ.get('NEWS_API_KEY') # read README 

if api_key is None:
    raise ValueError("API key not found in environment variables")

api = NewsDataApiClient(apikey=api_key)

def testNewsClient():
    response = api.news_api()
    print(response)

    # response = api.sources_api()
    # print(response)

def main():
    testNewsClient()

if __name__ == '__main__':
    main()
