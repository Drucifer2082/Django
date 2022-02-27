import requests

guardian_api_key = ""
historical_news_rapidapi_key: ""
google_news_rapidapi_key: ""
search =""
date = ""  

def theguardian_api(search):
  """API key and query search for the GuardianUK. The API stores all articles, images, audio and videos dating back to 1999"""
	url = f"https://content.guardianapis.com/search?q={search}&api-key={guardian_api_key}"
	guardian_results = requests.get(url)
	return guardian_results.json()

def historical_news_api(search):
  """API key and query search from Rapida API on historical news"""
	url = f"https://historical-news.p.rapidapi.com/search?q={search}&api-key={historical_news_rapidapi_key}"
	historical_news_results = requests.get(url)
	return historical_news_results.json()


def google_news_api(search):
"""Top stories, topic-related news feeds, a geolocation news feed, and an extensive full-text search feed"""
	url = f"https://google-news.p.rapidapi.com/search?q={search}&api-key={google_news_rapidapi_key}"
	google_news_results = requests.get(url)
	return google_news_results.json()





if __name__ == "__main__"
