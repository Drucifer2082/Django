from collections import namedtuple
import re

import requests

from bs4 import BeautifulSoup as bs

guardian_api_key = "725f716b-09bf-4971-816f-ef6b32061b1b"
nytimes_historical_api = "K6uJovBQ20GvZDB6e9wAWeoYO6m21rNY"
Article = namedtuple("Article", "title url")
HistoricArticle = namedtuple("HistoricArticle", "print_headline, section_name, lead_paragraph")
DailyNews = namedtuple("DailyNews", "title body")
top_headlines_api = "67a718ca0c904911b885f859c255dc21"
headers = {
    'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
    'x-rapidapi-key': "38c3a26bf6msh7b78364c9cb74afp18a2ddjsnef679721e0c0"
    }

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


def  _get_historical_news_search_data(search):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={search}&api-key={nytimes_historical_api}&show-blocks=all"
    query = requests.get(url)
    nytimes_historical_results = query.json()
    return nytimes_historical_results


def historical_news_api(search):
    resp = _get_historical_news_search_data(search)
    historical_articles = [
        HistoricArticle(art['headline']['print_headline'],
                        art['section_name'],
                        art['lead_paragraph'])
        for art in resp['response']['docs']
    ]
    return historical_articles


def the_selected_historical_news_article_text(nytimes_historical_results, html):
    page = requests.get(url)
    soup = bs(html, "html.parser")

    for data in soup(['style', 'script']):
        data.decompose()

        print(the_selected_historical_news_article_text(page.content))

def _daily_news(search):
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
    param_search = {"q":{search}}
    response = requests.get(url, headers=headers, params= param_search)
    text = response.json()
    article = text['value'][0]['body']
    art = re.sub('<[^<]+?>', '', article)
    return art

def daily_news(search):
    resp = _daily_news(search)
    daily_news_articles = [
            DailyNews(art['title'], art['body'])
                for art in resp['value']['body']
    ]
    return daily_news_articles

if __name__ == "__main__":
    # you can run this script as: $ python -m news.scraper
    url = ("https://content.guardianapis.com/world/2022/feb/03/"
           "turkish-president-erdogan-mediate-ukraine-russia")
    ret = parse_theguardian_article(url)
    print(ret)
