import requests
from bs4 import BeautifulSoup
import textwrap

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
    print(wrapped_text)
else:
    print("Article tag not found.")
