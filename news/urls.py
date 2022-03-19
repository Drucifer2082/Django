from django.contrib import admin
from django.urls import path

from .views import index
from .articles import Article

app_name = "news"
urlpatterns = [
    path("", index, name ="index"),
    path('articles/', views.articles)
]
htmx_urlpatterns = [
    path('search/', views.search_apis),
    path('articles/', views.articles)
]
urlpatterns += htmx_urlpatterns