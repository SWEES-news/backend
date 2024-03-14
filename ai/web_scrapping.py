import requests
from bs4 import BeautifulSoup
import textwrap
import logging

logging.basicConfig(level=logging.INFO)

def fetch_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX or 5XX errors
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

    return response.text

# A test URL of an article
url = 'https://www.engadget.com/the-morning-after-apples-car-project-may-be-dead-121513763.html'

# Fetch the content of the URL
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# Finding the article text
article = soup.find('article')
if article:
    article_text = article.get_text()

    # Wrap the extracted text to a maximum line width of 85 characters
    wrapped_text = textwrap.fill(article_text, width=85)

    with open('article_article_link.txt', 'w') as file:
        file.write(wrapped_text)
else:
    print("Article tag not found.")
