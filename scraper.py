import re

import requests

guardian_api_key = "725f716b-09bf-4971-816f-ef6b32061b1b"
historical_news_rapidapi_key = "38c3a26bf6msh7b78364c9cb74afp18a2ddjsnef679721e0c0"
google_news_rapidapi_key = "38c3a26bf6msh7b78364c9cb74afp18a2ddjsnef679721e0c0"


class NoContentException(Exception):
    pass


def get_theguardian_articles(search):
    """API key and query search for the GuardianUK. The API stores all articles, images, audio and videos dating back to 1999"""
    url = f"https://content.guardianapis.com/search?q={search}&api-key={guardian_api_key}"
    query = requests.get(url)
    guardian_results = query.json()
    return guardian_results


def parse_theguardian_article(url):
    url = f"{url}?api-key={guardian_api_key}&show-blocks=all"
    query = requests.get(url)
    ret = query.json()
    try:
        ret = ret["response"]["results"][0]["blocks"]['body'][0]['bodyHtml']
    except IndexError:
        raise NoContentException(f"cannot retrieve article content of {url}")
    # strip html tags off
    return re.sub('<[^<]+?>', '', ret)


def historical_news_api(search):
    """API key and query search from Rapida API on historical news"""
    url = "https://historical-news.p.rapidapi.com/reuters/2021-01-01/"
    headers = {
        'x-rapidapi-host': "historical-news.p.rapidapi.com",
        'x_rapidapi_key': historical_news_rapidapi_key
    }
    historical_news_results = requests.request("GET", url, headers=headers, params=search)

    return historical_news_results

def parse_historical_news_api(url)





def google_news_api(search):
    """Top stories, topic-related news feeds, a geolocation news feed, and an extensive full-text search feed"""
    url = "https://google-news.p.rapidapi.com/v1/top_headlines"
    headers = {
        'x-rapidapi-host': "google-news.p.rapidapi.com",
        'x-rapidapi-key': google_news_rapidapi_key
    }
    google_news_results = requests.request("GET", url, headers=headers, params=search)

    return google_news_results


if __name__ == "__main__":
    # you can run this script as: $ python -m news.scraper
    url = ("https://content.guardianapis.com/world/2022/feb/03/"
           "turkish-president-erdogan-mediate-ukraine-russia")
    ret = parse_theguardian_article(url)
    print(ret)
