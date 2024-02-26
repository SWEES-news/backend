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


def test_get_test_name():
    name = news._get_random_article()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = news._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == news.ID_LEN


def test_add_article_dup_name(temp_article):
    """
    Make sure a duplicate article name raises a ValueError.
    """
    dup_name = temp_article
    with pytest.raises(ValueError):
        news.add_article(dup_name, news.MOCK_LINK)


def test_add_article_blank_name():
    """
    Make sure a blank game name raises a ValueError.
    """
    with pytest.raises(ValueError):
        news.add_article('', news.MOCK_LINK)


def test_get_text_from_article_link():
    text = news.get_text_from_article_link(news.MOCK_LINK)
    assert isinstance(text, str)
    print(text)
    assert len(text) > 0


@pytest.mark.skip('the scrapping tool currently does not work')
def test_get_clean_text_from_article_link():
    body = news.get_clean_text_from_article_link(news.MOCK_LINK)
    assert isinstance(body, str)
    print(body)
    assert len(body) > 0
