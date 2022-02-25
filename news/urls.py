from django.contrib import admin
from django.urls import path

from .views import home

app_name = "news"
urlpatterns = [
    path("", home, name ="home")
]
