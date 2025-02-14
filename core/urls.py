# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('custom-category/create/', views.create_custom_category, name='create_custom_category'),
    path('custom-category/', views.custom_category_list, name='custom_category_list'),
]
