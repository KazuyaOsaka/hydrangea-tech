# newsaggregator/urls.py
from django.contrib import admin
from django.urls import path, include  # include をインポート
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('article/<int:id>/', views.article_detail, name='article_detail'),
    path('', include('core.urls')),  # core アプリの URL 設定を読み込む
    # 将来的な機能のためにランキングや設定ページのURLも追加できます
]
