from msilib.schema import ListView
from django.shortcuts import render

from history.scraper import daily_news, historical_news_api

from .models import Article

from news.scraper import get_theguardian_articles


def index(request):
    if request.method == "POST":
        search_term = request.POST["name"]
        articles = get_theguardian_articles(search_term), historical_news_api(search_term), daily_news(search_term)
        
    return render(request, "search.html")

class ArticleList(ListView):
    template_name = 'articles.html'
    model = Article
    context_object_name = 'articles'


def search_apis(request):
    search_api = request.POST.get("search")
    article = Article.objects.create(article=article)

    articles = request.article.all()
    return render(request, 'article.html', {'article': article})
    
