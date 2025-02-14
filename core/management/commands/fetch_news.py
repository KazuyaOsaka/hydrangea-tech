from django.core.management.base import BaseCommand
import feedparser
from core.models import NewsArticle
from datetime import datetime
import dateutil.parser

class Command(BaseCommand):
    help = 'Fetch news articles from an RSS feed and save them to the database.'

    def handle(self, *args, **kwargs):
        rss_url = 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries:
            title = entry.get('title', '')
            source_url = entry.get('link', '')
            published = entry.get('published', None)
            if published:
                publish_date = dateutil.parser.parse(published)
            else:
                publish_date = datetime.now()
            content = entry.get('summary', '')

            if not NewsArticle.objects.filter(title=title, publish_date=publish_date).exists():
                article = NewsArticle(
                    title=title,
                    source_url=source_url,
                    publish_date=publish_date,
                    content=content,
                    translated_content='',
                    category='Uncategorized',
                    country='USA'
                )
                article.save()
                self.stdout.write(self.style.SUCCESS(f'Saved article: {title}'))
            else:
                self.stdout.write(f'Article already exists: {title}')
        
        self.stdout.write(self.style.SUCCESS('Finished fetching news.'))
