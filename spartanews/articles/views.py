from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from datetime import datetime, timedelta

from .models import ContentInfo, CommentInfo
from .serializers import ArticleSerializer


# def article_point(dt, cm_cnt, like_cnt):
#     # dt: create_dt
#     # cm_cnt: comments count
#     # like_cnt: article(content) likes count
#     now = datetime.now()
#
#     return -5 * (now - dt).days + 3 * cm_cnt + like_cnt


class ArticleAPIView(APIView):

    def get(self, request):
        rows = ContentInfo.objects.filter(is_visible=True)
        serializer = ArticleSerializer(rows, many=True)
        return Response(serializer.data)
