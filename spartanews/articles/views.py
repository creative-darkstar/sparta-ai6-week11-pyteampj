from django.shortcuts import get_object_or_404
from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ContentSerializer
from .models import ContentInfo, CommentInfo


class ContentListAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        rows = ContentInfo.objects.filter(is_visible=True)
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

class BookmarkAPIView(generics.UpdateAPIView):
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