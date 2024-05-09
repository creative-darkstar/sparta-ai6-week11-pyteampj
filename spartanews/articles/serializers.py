from rest_framework import serializers
from .models import ContentInfo, CommentInfo
from datetime import datetime, timedelta


class ContentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="userinfo.username", read_only=True)
    comment_count = serializers.IntegerField()
    like_count = serializers.IntegerField()
    article_point = serializers.IntegerField()

    class Meta:
        model = ContentInfo
        fields = '__all__'
        read_only_fields = (
            "userinfo",
            "is_visible",
            "comment_count",
            "like_count",
            "article_point",
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("userinfo")
        ret.pop("is_visible")
        return ret
