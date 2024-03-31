import requests
from bs4 import BeautifulSoup
import textwrap
import logging

logging.basicConfig(level=logging.INFO)


def fetch_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises exception for 4XX or 5XX errors
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

    return response.text


def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

    # Extract author
    author_tag = soup.find(class_='author')  # Adjust class as needed
    author = author_tag.get_text(strip=True) if author_tag else "No Author Found"

    # Extract article text
    article = soup.find('article')
    if not article:
        logging.warning("Article tag not found.")
        return None

    article_text = article.get_text(strip=True)

    return title, author, article_text


def save_article(title, author, article_text, filename='article.txt', width=85):
    with open(filename, 'w') as file:
        file.write(f"Title: {title}\n")
        file.write(f"Author: {author}\n")
        file.write("Article Body:\n")
        wrapped_text = textwrap.fill(article_text, width=width)
        file.write(wrapped_text)


def main(url):
    html_content = fetch_article_content(url)
    if html_content:
        title, author, article_text = extract_content(html_content)
        if article_text:
            save_article(title, author, article_text)


if __name__ == "__main__":
    url = ('https://www.engadget.com/the-morning-after-apples-car-project-'
           'may-be-dead-121513763.html')
    main(url)
