from django.shortcuts import render

from .models import Article

from news.scraper import get_theguardian_articles


def index(request):
    if request.method == "POST":
        search_term = request.POST["name"]
        articles = get_theguardian_articles(search_term)
        # articles don't have content, so we made parse_theguardian_article
        # in scraper.py
        breakpoint()

    return render(request, "search.html")
