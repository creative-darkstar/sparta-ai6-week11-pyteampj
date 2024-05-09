from django.urls import path
from . import views
from .views import PostLikeAPIView , BookmarkAPIView

app_name = 'articles'
urlpatterns = [
    path("", views.ContentListAPIView.as_view(), name="content_list"),
    path("<int:content_id>/", views.ContentDetailAPIView.as_view(), name="content_detail"),
    path("<int:content_id>/like", PostLikeAPIView.as_view(), name="like"),
    path("<int:content_id>/bookmark", BookmarkAPIView.as_view(), name="bookmark"),
]
