from subprocess import IDLE_PRIORITY_CLASS
from django.shortcuts import render

# Create your views here.
def index(response, id):
    ls = NewsList.objects.get(id=id)
    return render(response, "main/list.html", {"ls":ls})


def home(response):
    return render(response, "main/home.html", {})