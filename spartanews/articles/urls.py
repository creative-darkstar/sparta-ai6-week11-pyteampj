from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path("", views.ContentListAPIView.as_view(), name="content_list"),
    path("<int:content_id>/", views.ContentDetailAPIView.as_view(), name="content_detail"),
]
