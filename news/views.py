from django.shortcuts import render

from .models import Article


def index(response):
    articles = Article.objects.all()
    # TODO:
    """
    1. we need to put the api scraping code in django
    2. call it and populate db articles table
    3. v) we already retrieve them in the view
    4. display articles in view
    5. look at django forms to have a user do a search
    """
    return render(response, "main/list.html", {"articles": articles})


def home(response):
    return render(response, "main/home.html", {})
