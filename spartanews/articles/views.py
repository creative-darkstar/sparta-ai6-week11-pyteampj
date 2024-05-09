# Django modules
from django.db.models import (
    F, Q, Count, Func, ExpressionWrapper,
    DateTimeField,
    DurationField,
    IntegerField,
)
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from django.utils import timezone

# DRF modules
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# serializers and models
from .serializers import ContentSerializer
from .models import ContentInfo, CommentInfo


class InvalidQueryParamsException(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "Your request contain invalid query parameters."


class ContentListAPIView(generics.ListAPIView):
    serializer_class = ContentSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query_params = self.request.query_params

        # value of ordering query string
        order_by = query_params.get("order-by")

        # value of filtering query string
        user = query_params.get("user")
        liked_by = query_params.get("liked-by")
        favorite_by = query_params.get("favorite-by")

        # get rows from table 'ContentInfo'
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

        # Filtering
        # create Q object
        q = Q()

        # check 'user' query string
        if user is not None:
            if user.isdecimal():
                q &= Q(userinfo_id=int(user))
            else:
                raise InvalidQueryParamsException

        # check 'liked_by' query string
        if liked_by is not None:
            if liked_by.isdecimal():
                q &= Q(liked_by=int(liked_by))
            else:
                raise InvalidQueryParamsException

        # check 'favorite_by' query string
        if favorite_by is not None:
            if favorite_by.isdecimal():
                q &= Q(favorite_by=int(favorite_by))
            else:
                raise InvalidQueryParamsException

        return rows.filter(q)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                userinfo=request.user,
                is_visible=True
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContentDetailAPIView(APIView):

    # permission_classes = [IsAuthenticated]

    def get_object(self, content_id):
        return get_object_or_404(ContentInfo, pk=content_id)

    def get(self, request, content_id):
        content = self.get_object(content_id)
        serializer = ContentSerializer(content)
        return Response(serializer.data)
    
    def put(self, request, content_id):
        content = self.get_object(content_id)
        serializer = ContentSerializer(content, data=request.data ,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, content_id):
        content = self.get_object(content_id)
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PostLikeAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = ContentInfo.objects.all()
    serializer_class = ContentSerializer
    lookup_field = 'id'

    def post(self, request, pk):
        instance = get_object_or_404(ContentInfo, pk=pk)
        user = request.user
        if user in instance.bookmarked_by.all():
            instance.bookmarked_by.remove(user)
            instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            instance.bookmarked_by.add(user)
            instance.save()
            return Response(status=status.HTTP_201_CREATED)

