from rest_framework import serializers
from .models import ContentInfo


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentInfo
        fields = "__all__"
