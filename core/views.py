# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from core.models import NewsArticle, CustomCategory
from .forms import CustomCategoryForm

def home(request):
    articles = NewsArticle.objects.order_by('-publish_date')
    return render(request, 'home.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(NewsArticle, id=id)
    return render(request, 'article_detail.html', {'article': article})

def create_custom_category(request):
    if request.method == "POST":
        form = CustomCategoryForm(request.POST)
        if form.is_valid():
            custom_category = form.save(commit=False)
            custom_category.user = request.user  # ログインユーザーに紐づけ
            custom_category.save()
            return redirect('custom_category_list')
    else:
        form = CustomCategoryForm()
    return render(request, 'custom_category_form.html', {'form': form})

def custom_category_list(request):
    categories = CustomCategory.objects.filter(user=request.user)
    return render(request, 'custom_category_list.html', {'categories': categories})
