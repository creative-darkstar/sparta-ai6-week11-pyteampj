from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path("", views.ContentListAPIView.as_view(), name="content_list"),
    path("<int:content_id>/", views.ContentDetailAPIView.as_view(), name="content_detail"),
    path("<int:content_id>/like", views.PostLikeAPIView.as_view(), name="content_like"),
    path("<int:content_id>/favorite", views.BookmarkAPIView.as_view(), name="content_favorite"),
    path("<int:content_id>/comment", views.CommentListAPIView.as_view(), name="comment_list"),
    path("comment/<int:comment_id>", views.CommentDetailAPIView.as_view(), name="comment_detail"),
]
