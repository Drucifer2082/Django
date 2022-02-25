from django.shortcuts import render

from .models import Article


def index(response, id):
    article = Article.objects.get(id=id)
    return render(response, "main/list.html", {"article": article})


def home(response):
    return render(response, "main/home.html", {})
