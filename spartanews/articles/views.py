from django.db.models import F, Count, ExpressionWrapper, DurationField
from django.db.models.functions import Now, Extract, Cast
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ContentSerializer
from .models import ContentInfo, CommentInfo



from datetime import datetime, timedelta
def article_point(create_dt, cm_cnt, like_cnt):
    # create_dt: create_dt
    # cm_cnt: comments count
    # like_cnt: article(content) likes count

    print(create_dt, cm_cnt, like_cnt)
    now = datetime.now()
    return -5 * (now - create_dt).days + 3 * cm_cnt + like_cnt


class ContentListAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = ContentInfo.objects.filter(is_visible=True)
        rows = rows.annotate(
            comment_count=Count(F("related_content")),
            like_count=Count(F("liked_by")),
            duration=F("create_dt")
        )
        for row in rows:
            print(row.comment_count, row.like_count, row.duration)
        serializer = ContentSerializer(rows, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContentDetailAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get_object(self, content_id):
        return get_object_or_404(ContentInfo, pk=content_id)

    def get(self, request, content_id):
        content = self.get_object(content_id)
        serializer = ContentSerializer(content)
        return Response(serializer.data)
    
    def put(self, request, content_id):
        content = self.get_object(content_id)
        serializer = ContentSerializer(content, data=request.data ,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, content_id):
        content = self.get_object(content_id)
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PostLikeAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = ContentInfo.objects.all()
    serializer_class = ContentSerializer
    lookup_field = 'id'

    def post(self, request, pk):
        instance = get_object_or_404(ContentInfo, pk=pk)
        user = request.user
        if user in instance.bookmarked_by.all():
            instance.bookmarked_by.remove(user)
            instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            instance.bookmarked_by.add(user)
            instance.save()
            return Response(status=status.HTTP_201_CREATED)

