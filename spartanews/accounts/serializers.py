from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserInfo
from articles.models import ContentInfo, CommentInfo


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "date_joined",
            "introduction",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["favorite_contents_url"] = f"api/content/?favorite-by={instance.id}"
        ret["liked_contents_url"] = f"api/content/?liked-by={instance.id}"
        ret["liked_comments_url"] = f"api/content/comment/?liked-by={instance.id}"
        return ret










# class UserSelfSerializer(serializers.ModelSerializer):
#     favorite_contents = FavoriteContentSerializer(many=True)
#     liked_contents = LikedContentSerializer(many=True)
#     liked_comments = LikedCommentSerializer(many=True)
#     # user_contents = UserContentSerializer(many=True)
#     # user_comments = UserCommentSerializer(many=True)

#     class Meta:
#         model = get_user_model()
#         fields = [
#             "id",
#             "username",
#             "date_joined",
#             "introduction",
#             # "user_contents",
#             # "user_comments",
#             "favorite_contents",
#             "liked_contents",
#             "liked_comments",
#         ]