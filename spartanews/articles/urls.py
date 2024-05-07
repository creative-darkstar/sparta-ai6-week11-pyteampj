from django.urls import path
from .views import ArticleAPIView

app_name = 'articles'

urlpatterns = [
    path("", ArticleAPIView.as_view(), name='article_all'),
]
