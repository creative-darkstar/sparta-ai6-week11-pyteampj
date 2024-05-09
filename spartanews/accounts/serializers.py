from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    # ManyToMany
    contents = ContentSerializer(read_only = True, many=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "date_joined",
            "introduction",
        ]