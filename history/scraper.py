from collections import namedtuple
import re

import requests

guardian_api_key = "725f716b-09bf-4971-816f-ef6b32061b1b"
nytimes_historical_api = "K6uJovBQ20GvZDB6e9wAWeoYO6m21rNY"
Article = namedtuple("Article", "title url")
HistoricArticle = namedtuple("HistoricArticle", "print_headline, section_name, lead_paragraph")
top_headlines_api ="67a718ca0c904911b885f859c255dc21"

class NoContentException(Exception):
    pass


def _get_theguardian_search_data(search):
    """API key and query search for the GuardianUK. The API stores all articles, images, audio and videos dating back to 1999"""
    url = f"https://content.guardianapis.com/search?q={search}&api-key={guardian_api_key}"
    query = requests.get(url)
    resp = query.json()
    return resp


def get_theguardian_articles(search):
    resp = _get_theguardian_search_data(search)
    articles = [Article(art["webTitle"], art["apiUrl"])
                 for art in resp["response"]["results"]]
    return articles


def parse_theguardian_article(url):
    if "api-key" not in url:
        url += f"?api-key={guardian_api_key}&show-blocks=all"
    query = requests.get(url)
    resp = query.json()
    try:
        ret = resp["response"]["content"]["blocks"]['body'][0]['bodyHtml']
    except (IndexError, KeyError):
        raise NoContentException(f"cannot retrieve article content of {url}")
    # strip html tags off
    article = re.sub('<[^<]+?>', '', ret)
    return article


def historical_news_api(search):
    resp = _get_historical_news_search_data(search)
    """
    historical_articles = [HistoricArticle(art['headline']['print_headline'], art['section_name'], art            ['lead_paragraph'])
                    for art in resp['response']['docs'][0]]
    """
    # TODO: scrape them!
    historical_articles = [
        row["lead_paragraph"] for row in
        resp['response']['docs']
    ]
    return historical_articles

def  _get_historical_news_search_data(search):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={search}&api-key={nytimes_historical_api}&show-blocks=all"
    query = requests.get(url)
    nytimes_historical_results = query.json()
    return nytimes_historical_results

def daily_top_headlines():
    """ shows live headlines in near real time."""
    url = (f'https://newsapi.org/v2/top-headlines?'
           'country=us&'
           'apiKey={top_headlines_api}')
    response = requests.get(url)
    top_headlines = response.json()
    return top_headlines

def parse_daily_top_headlines_titles():
    url = url = ('https://newsapi.org/v2/top-headlines?'
           'country=us&'
           'apiKey={top_headlines_api}')
    query = requests.get(url)
    ret = query.json()
    try:
        ret = ret["articles"][0]['title']
    except IndexError:
        raise NoContentException(f"cannot retrieve article content of {url}")
    # strip html tags off
    return re.sub('<[^<]+?>', '', ret)

def parse_daily_top_headlines_content():
    url = url = ('https://newsapi.org/v2/top-headlines?'
           'country=us&'
           'apiKey=67a718ca0c904911b885f859c255dc21')
    query = requests.get(url)
    ret = query.json()
    try:
        ret = ret['articles'][0]['content']
    except IndexError:
        raise NoContentException(f"cannot retrieve article content of {url}")
    # strip html tags off
    return re.sub('<[^<]+?>', '', ret)

if __name__ == "__main__":
    # you can run this script as: $ python -m news.scraper
    url = ("https://content.guardianapis.com/world/2022/feb/03/"
           "turkish-president-erdogan-mediate-ukraine-russia")
    ret = parse_theguardian_article(url)
    print(ret)
