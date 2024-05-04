from django.conf import settings
from django.db import models


class ContentInfo(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('N', "News"),
        ('A', "Ask"),
        ('S', "Show"),
    )

    userinfo = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contents"
    )
    title = models.CharField(max_length=50)
    content = models.TextField()
    content_type = models.CharField(
        max_length=2,
        choices=CONTENT_TYPE_CHOICES,
        default='N'
    )
    url = models.URLField(null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)


class CommentInfo(models.Model):
    userinfo = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    contentinfo = models.ForeignKey(
        ContentInfo, on_delete=models.CASCADE, related_name="related_content"
    )
    content = models.TextField()
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now=True)
