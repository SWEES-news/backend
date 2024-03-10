"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import random
import requests
import html2text
from bs4 import BeautifulSoup
from cleantext import clean

ID_LEN = 24
BIG_NUM = 100000000000000000000
MOCK_ID = '0' * ID_LEN
MAX_NAME_LEN = 320
NAME = 'Title'
MOCK_NAME = 'test'
NAME = 'NAME'
LINK = 'LINK'
MOCK_LINK_FRONT = 'https://www.vice.com/en/article/jg877g/brazilian-'
MOCK_LINK_BACK = 'prosecutor-accused-of-spreading-nazi-propaganda-facebook'
MOCK_LINK = MOCK_LINK_FRONT + MOCK_LINK_BACK
USER_ID = 'USER_ID'

# storage of articles, NAME: tuple(articlename, password)
articles = {
    MOCK_NAME: {NAME: MOCK_NAME, LINK: MOCK_LINK}
}


# returns json of mock article
def get_test_article():
    return {NAME: MOCK_NAME, LINK: MOCK_LINK, USER_ID: MOCK_ID}


# returns a randomly generated mock NAME
def _get_random_article():
    rand_part = str(random.randint(0, BIG_NUM))
    if len(rand_part) > MAX_NAME_LEN:
        rand_str = (rand_part[:MAX_NAME_LEN])
    else:
        rand_str = rand_part
    return rand_str


# gets a article with a random gmail address
def get_rand_test_article():
    rand_part = _get_random_article()
    return {NAME: rand_part, LINK: MOCK_LINK}


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_articles() -> dict:
    articles = {'article1': get_test_article(),
                'article2': get_test_article()}
    return articles


def add_article(name: str, link: str) -> str:
    if name in articles:
        raise ValueError(f'Duplicate name: {name=}')
    if not name:
        raise ValueError('name may not be blank')
    articles[name] = {NAME: name, LINK: link}
    return _gen_id()


def get_name(article):
    return article.get(NAME, '')


def exists(name: str) -> bool:
    return name in get_articles()


def get_article_by_id(article_id: str):
    """
    Fetches a article from the database by their ID.
    """
    global client
    db = client.your_database_name
    articles_collection = db.articles
    article = articles_collection.find_one({'_id': article_id})
    return article


def get_text_from_article_link(link: str):
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


def get_clean_text_from_article_link(link: str):
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
