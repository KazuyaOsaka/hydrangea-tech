# core/views.py
from django.shortcuts import render, get_object_or_404
from core.models import NewsArticle

def home(request):
    articles = NewsArticle.objects.order_by('-publish_date')
    return render(request, 'home.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    return render(request, 'article_detail.html', {'article': article})
