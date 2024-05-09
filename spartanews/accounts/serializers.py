from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserInfo
from articles.models import ContentInfo


class FavoriteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["favorite_contents"]


class LikedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["liked_contents"]


class LikedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["liked_commments"]


class UserSerializer(serializers.ModelSerializer):
    favorite_contents = FavoriteContentSerializer(many=True)
    liked_contents = LikedContentSerializer(many=True)
    liked_comments = LikedCommentSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "introduction",
            "favorite_contents",
            "liked_contents",
            "liked_comments"
        ]