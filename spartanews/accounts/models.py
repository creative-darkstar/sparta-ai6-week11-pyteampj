from django.db import models
from django.contrib.auth.models import AbstractUser
from articles.models import ContentInfo, CommentInfo


class UserInfo(AbstractUser):
    introduction = models.TextField(null=True, blank=True)

    favorite_contents = models.ManyToManyField(
        ContentInfo, related_name='favorite_by', blank=True
    )

    liked_contents = models.ManyToManyField(
        ContentInfo, related_name='liked_by', blank=True
    )

    liked_comments = models.ManyToManyField(
        CommentInfo, related_name='liked_by', blank=True
    )
