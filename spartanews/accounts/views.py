from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

class SignupAPIView(APIView):
    def post(self, request):
        data = request.data

        username = data.get("username")
        email = data.get("email")

        user = get_user_model().objects.create_user(
            username = username,
            email = email,
            password = data.get("password"),
            introduction = data.get("introduction")
        )

        return Response(
            {
                "username": user.username,
                "message": "회원가입이 완료되었습니다."
            },
            status = status.HTTP_201_CREATED
        )