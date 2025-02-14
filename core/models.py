from django.conf import settings
from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    source_url = models.URLField()
    publish_date = models.DateTimeField()
    content = models.TextField()
    translated_content = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class CustomCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="カスタムカテゴリ名")
    keywords = models.TextField(help_text="カンマ区切りでキーワードを入力してください")

    def __str__(self):
        return self.name
