from django.db import models

from history.scraper import DailyNews


class Article(models.Model):
    GUARDIAN_UK = "gu"
    HISTORIC_NEWS = "hn"
    GOOGLE = "go"
    SOURCES = [
        (GUARDIAN_UK, "Guardian UK"),
        (HISTORIC_NEWS, "NY Times"),
        (DailyNews, "Al Jazeera"),
    ]
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    description = models.TextField()
    link = models.URLField()
    source = models.CharField(
        max_length=2,
        choices=SOURCES,
        default=GUARDIAN_UK,
    )
    added = models.DateTimeField(auto_now_add=True)
