from rest_framework import serializers
from .models import ContentInfo, CommentInfo
from datetime import datetime, timedelta

def article_point(create_dt, cm_cnt, like_cnt):
    # create_dt: create_dt
    # cm_cnt: comments count
    # like_cnt: article(content) likes count

    now = datetime.now()
    return -5 * (now - create_dt).days + 3 * cm_cnt + like_cnt


class ContentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="userinfo.username", read_only=True)
    comment_count = serializers.IntegerField(source="related_content.count", read_only=True)
    like_count = serializers.IntegerField(source="userinfo.liked_contents.count", read_only=True)

    class Meta:
        model = ContentInfo
        fields = '__all__'
        read_only_fields = (
            "userinfo",
            "is_visible",
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["article_point"] = article_point(
            create_dt=instance.create_dt.replace(tzinfo=None),
            cm_cnt=ret["comment_count"],
            like_cnt=ret["like_count"]
        )
        ret.pop("userinfo")
        ret.pop("is_visible")
        return ret
