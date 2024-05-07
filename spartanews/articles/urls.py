from django.urls import path
from . import views



app_name = 'articles'
urlpatterns = [
    path("", views.ContentListAPIView.as_view(), name="product_detail"),
]
