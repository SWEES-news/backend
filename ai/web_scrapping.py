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

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    article = soup.find('article')
    if not article:
        logging.warning("Article tag not found.")
        return None
    
    return article.get_text()

def save_article(text, filename='article.txt', width=85):
    wrapped_text = textwrap.fill(text, width=width)
    with open(filename, 'w') as file:
        file.write(wrapped_text)
