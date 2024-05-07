from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContentInfo, CommentInfo
from .serializers import ArticleSerializer


class ArticleAPIView(APIView):

    def get(self, request):
        rows = ContentInfo.objects.filter(is_visible=True)
        serializer = ArticleSerializer(rows, many=True)
        return Response(serializer.data)
