from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ContentSerializer
from django.shortcuts import get_object_or_404
from .models import ContentInfo



class ContentListAPIView(APIView):

    # permission_classes = [IsAuthenticated]

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
    
