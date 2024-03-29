"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import requests
import html2text
from bs4 import BeautifulSoup
from cleantext import clean


def get_text_from_article_link(link: str):
    """
    Fetches and cleans the text from a news website.

    It does not manage to clean all data, but should do a good enough
    job for a good language model to not have issues with it.

    :param link: The link to the article.
    :return: A cleaned string of the article.
    """
    response = requests.get(link)
    html_str = response.content
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    text = h.handle(str(html_str))
    text = clean(text, no_emails=True, no_phone_numbers=True)
    splitText = text.splitlines()
    # print(splitText)
    textLen = len(splitText)
    i = 0
    newList = []
    charDict = {
        r'"': 0,
        '[': 1,
        '(': 2
    }
    while i < textLen:
        # print(len(splitText[i]))
        if len(splitText[i]) == 0:
            del splitText[i]
            textLen -= 1
        elif not splitText[i][0].isalnum() and not splitText[i][0] in charDict:
            print(str(i) + ': ' + splitText[i])
        else:
            newList.append(splitText[i])
        i += 1
    # print(splitText)
    newText = '\n'.join(newList)
    return newText


def clean_text(text: str):
    """
    cleans a string.

    It does not manage to clean all data, but should do a good enough
    job for a good language model to not have issues with it.

    :param text: Raw text pasted by the user.
    :return: A cleaned string of the article.
    """
    text = clean(text, no_emails=True, no_phone_numbers=True)
    splitText = text.splitlines()
    # print(splitText)
    textLen = len(splitText)
    i = 0
    newList = []
    charDict = {
        r'"': 0,
        '[': 1,
        '(': 2
    }
    while i < textLen:
        # print(len(splitText[i]))
        if len(splitText[i]) == 0:
            del splitText[i]
            textLen -= 1
        elif not splitText[i][0].isalnum() and not splitText[i][0] in charDict:
            print(str(i) + ': ' + splitText[i])
        else:
            newList.append(splitText[i])
        i += 1
    # print(splitText)
    newText = '\n'.join(newList)
    return newText


def get_clean_text_from_article_link(link: str):
    """
    This function currently does not work as indended, due to differing
    naming conventions across websites. it can be fine tuned later
    to clean text from specific websites, but the current option
    appears to be better
    """
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')
    title = soup.find('title')
    print(title.get_text())
    author = soup.find('small',  itemprop="author")
    # container = soup.find('div',
    # class_=['entry-content', 'entry-content-read-more'])
    # articletext = container.find_all('p')
    articletext = soup.find_all('p')
    print(articletext)
    body = ''
    for paragraph in articletext[:-1]:
        text = paragraph.get_text()
        body += text
    return title, author, body
