from django.shortcuts import render
from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContentInfo, CommentInfo
from .serializers import ArticleSerializer


# class ArticleAPIView(generics.ListAPIView):
#     serializer_class = ArticleSerializer
#     filter_backends = [filters.OrderingFilter]
#     # ordering_fields = [
#     #     "article_point",
#     #     "-create_dt",
#     # ]
#     ordering = [
#         "article_point",
#         "-create_dt",
#     ]
#
#     def get_queryset(self):
#         query_params = self.request.query_params
#         order_by = query_params.get("order-by")
#         user = query_params.get("user")
#         liked_by = query_params.get("liked-by")
#         favorite_by = query_params.get("favorite-by")
#
#         if order_by == "new":
#             self.ordering.remove("article_point")
#             print(self.ordering)
#         else:
#             self.ordering.remove("-create_dt")
#             print(self.ordering)
#
#         return ContentInfo.objects.all()


class ArticleAPIView(APIView):

    def get(self, request):
        rows = ContentInfo.objects.filter(is_visible=True)
        serializer = ArticleSerializer(rows, many=True)
        return Response(serializer.data)
