# Django modules
from django.contrib.auth import get_user_model
from django.db.models import (
    F, Count, Func, ExpressionWrapper,
    DateTimeField,
    DurationField,
    IntegerField,
)
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from django.utils import timezone

# DRF modules
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# serializers and models
from .serializers import (
    ContentSerializer,
    ContentAllSerializer,
    CommentSerializer,
)
from .models import ContentInfo, CommentInfo


# Custom API exception class when request with unavailable query params
class InvalidQueryParamsException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "Your request contain invalid query parameters."


# Custom pagination class for articles list
class ArticlesListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# Custom pagination class for an article's comments list
class CommentsListPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50


class ContentListAPIView(generics.ListAPIView):
    serializer_class = ContentAllSerializer
    pagination_class = ArticlesListPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query_params = self.request.query_params

        # value of ordering query string
        order_by = query_params.get("order-by")

        # value of filtering query string
        favorite_by = query_params.get("favorite-by")
        liked_by = query_params.get("liked-by")
        user = query_params.get("user")

        # Filtering

        # check 'favorite_by' query string
        # UserInfo.favorite_contents
        if favorite_by:
            if favorite_by.isdecimal():
                rows = get_user_model().objects.get(pk=int(favorite_by)).favorite_contents.filter(is_visible=True)
            else:
                raise InvalidQueryParamsException
        # check 'liked_by' query string
        # UserInfo.liked_contents
        elif liked_by:
            if liked_by.isdecimal():
                rows = get_user_model().objects.get(pk=int(liked_by)).liked_contents.filter(is_visible=True)
            else:
                raise InvalidQueryParamsException
        # check 'user' query string
        # ContentInfo
        elif user:
            if user.isdecimal():
                rows = ContentInfo.objects.filter(is_visible=True, userinfo_id=int(user))
            else:
                raise InvalidQueryParamsException
        # no query string
        # ContentInfo
        else:
            rows = ContentInfo.objects.filter(is_visible=True)

        # annotate fields: 'comment_count', 'like_count', 'article_point'
        # annotate but not include in serialized data: 'duration_in_microseconds', 'duration'
        # duration_in_microseconds is divided by (1000 * 1000 * 60 * 60 * 24)
        # because of converting microseconds to days
        rows = rows.annotate(
            comment_count=Count(F("comments_on_content")),
            like_count=Count(F("liked_by")),
            duration_in_microseconds=ExpressionWrapper(
                Cast(timezone.now().replace(microsecond=0), DateTimeField()) - F("create_dt"),
                output_field=DurationField()
            )
        ).annotate(
            duration=ExpressionWrapper(
                Func(
                    F('duration_in_microseconds') / (1000 * 1000 * 60 * 60 * 24),
                    function='FLOOR',
                    template="%(function)s(%(expressions)s)"
                ),
                output_field=IntegerField()
            )
        ).annotate(
            article_point=ExpressionWrapper(
                -5 * F("duration") + 3 * F("comment_count") + F("like_count"),
                output_field=IntegerField()
            )
        )

        # Ordering
        # order-by=new: ORDER BY create_dt DESC
        # nothing: ORDER BY article_point DESC create_dt DESC
        if order_by == "new":
            rows = rows.order_by("-create_dt")
        else:
            rows = rows.order_by("-article_point", "-create_dt")

        return rows

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                userinfo=request.user,
                is_visible=True
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContentDetailAPIView(generics.ListAPIView):
    serializer_class = ContentAllSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_row(self, content_id):
        return get_object_or_404(ContentInfo, pk=content_id)

    def get_queryset(self):
        row = ContentInfo.objects.filter(pk=self.kwargs.get("content_id"), is_visible=True)
        if not row:
            return ContentInfo.objects.none()

        # annotate fields: 'comment_count', 'like_count', 'article_point'
        # annotate but not include in serialized data: 'duration_in_microseconds', 'duration'
        # duration_in_microseconds is divided by (1000 * 1000 * 60 * 60 * 24)
        # because of converting microseconds to days
        row = row.annotate(
            comment_count=Count(F("comments_on_content")),
            like_count=Count(F("liked_by")),
            duration_in_microseconds=ExpressionWrapper(
                Cast(timezone.now().replace(microsecond=0), DateTimeField()) - F("create_dt"),
                output_field=DurationField()
            )
        ).annotate(
            duration=ExpressionWrapper(
                Func(
                    F('duration_in_microseconds') / (1000 * 1000 * 60 * 60 * 24),
                    function='FLOOR',
                    template="%(function)s(%(expressions)s)"
                ),
                output_field=IntegerField()
            )
        ).annotate(
            article_point=ExpressionWrapper(
                -5 * F("duration") + 3 * F("comment_count") + F("like_count"),
                output_field=IntegerField()
            )
        )

        return row
    
    def put(self, request, content_id):
        row = self.get_row(content_id)
        # 로그인한 사용자와 글 작성자가 다를 경우 상태코드 403
        if request.user.id != row.userinfo.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ContentSerializer(row, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, content_id):
        row = self.get_row(content_id)
        # 로그인한 사용자와 글 작성자가 다를 경우 상태코드 403
        if request.user.id != row.userinfo.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # soft delete
        # 삭제된 글 추적을 위함
        row.is_visible = False
        row.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentsListPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # endpoint: /api/content/<int:content_id>/comment
        content_id = self.kwargs.get("content_id")
        # check 'content_id' parameter
        # CommentInfo
        if content_id:
            rows = CommentInfo.objects.filter(contentinfo_id=content_id, is_visible=True)
            # order by earliest
            return rows.order_by("create_dt")

        # endpoint: /api/content/comment
        liked_by = self.request.GET.get("liked-by")
        user = self.request.GET.get("user")
        # check 'liked_by' query string
        # UserInfo.liked_comments
        if liked_by:
            if liked_by.isdecimal():
                rows = get_user_model().objects.get(pk=int(liked_by)).liked_comments.filter(is_visible=True)
            else:
                raise InvalidQueryParamsException
        # check 'user' query string
        # CommentInfo
        elif user:
            if user.isdecimal():
                rows = CommentInfo.objects.filter(is_visible=True, userinfo_id=int(user))
            else:
                raise InvalidQueryParamsException
        # no query string
        # CommentInfo
        else:
            rows = CommentInfo.objects.filter(is_visible=True)

        # order by latest
        return rows.order_by("-create_dt")


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_row(self, comment_id):
        return get_object_or_404(CommentInfo, pk=comment_id)

    def put(self, request, comment_id):
        row = self.get_row(comment_id)
        # 로그인한 사용자와 댓글 작성자가 다를 경우 상태코드 403
        if request.user.id != row.userinfo.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(row, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, comment_id):
        row = self.get_row(comment_id)
        # 로그인한 사용자와 댓글 작성자가 다를 경우 상태코드 403
        if request.user.id != row.userinfo.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # soft delete
        # 삭제된 댓글 추적을 위함
        row.is_visible = False
        row.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def content_favorite(request, content_id):
    if request.user.is_authenticated:
        me = get_user_model().objects.get(id=request.user.id)
        content = get_object_or_404(ContentInfo, id=content_id)

        if me.favorite_contents.filter(id=content_id).exists():
            me.favorite_contents.remove(content)
            return Response(
                data={
                    "message": "Favorite content canceled.",
                },
                status=status.HTTP_200_OK
            )
        else:
            me.favorite_contents.add(content)
            return Response(
                data={
                    "message": "Favorite content success.",
                    "user": me.username,
                    "content_id": content.id,
                },
                status=status.HTTP_200_OK
            )
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def content_like(request, content_id):
    if request.user.is_authenticated:
        me = get_user_model().objects.get(id=request.user.id)
        content = get_object_or_404(ContentInfo, id=content_id)

        if me.liked_contents.filter(id=content_id).exists():
            me.liked_contents.remove(content)
            return Response(
                data={
                    "message": "Like content canceled.",
                },
                status=status.HTTP_200_OK
            )
        else:
            me.liked_contents.add(content)
            return Response(
                data={
                    "message": "Like content success.",
                    "user": me.username,
                    "content_id": content.id,
                },
                status=status.HTTP_200_OK
            )
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def comment_like(request, comment_id):
    if request.user.is_authenticated:
        me = get_user_model().objects.get(id=request.user.id)
        comment = get_object_or_404(CommentInfo, id=comment_id)

        if me.liked_comments.filter(id=comment_id).exists():
            me.liked_comments.remove(comment)
            return Response(
                data={
                    "message": "Like comment canceled.",
                },
                status=status.HTTP_200_OK
            )
        else:
            me.liked_comments.add(comment)
            return Response(
                data={
                    "message": "Like comment success.",
                    "user": me.username,
                    "content_id": comment.id,
                },
                status=status.HTTP_200_OK
            )
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
