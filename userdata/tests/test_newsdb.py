import pytest

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import newsdb as news

@pytest.fixture(scope='function')
def temp_article():
    name = news._get_random_article()
    ret = news.add_article(name, news.MOCK_LINK)
    return name
    # delete the article!


def test_get_test_email():
    name = news._get_random_article()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = news._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == news.ID_LEN


def test_get_test_article():
    assert isinstance(news.get_rand_test_article(), dict)


def test_get_articles():
    articles = news.get_articles()
    assert isinstance(articles, dict)
    assert len(articles) > 0
    for article in articles:
        assert isinstance(article, str)
        assert isinstance(articles[article], dict)
    assert news.MOCK_NAME in articles


def test_add_article_dup_email(temp_article):
    """
    Make sure a duplicate article email raises a ValueError.
    """
    dup_name = temp_article
    with pytest.raises(ValueError):
        news.add_article(dup_name, news.MOCK_LINK)


def test_add_article_blank_email():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        news.add_article('', news.MOCK_LINK)


ADD_NAME = 'Crazy News'


def test_add_article():
    ret = news.add_article(ADD_NAME, news.MOCK_LINK)
    assert news.exists(ADD_NAME)
    assert isinstance(ret, str)