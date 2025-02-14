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
