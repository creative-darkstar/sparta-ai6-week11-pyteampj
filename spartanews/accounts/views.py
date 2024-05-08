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

        if not username or not email:
            return Response(
                {
                    "message":"필수 항목을 입력하여 주십시오."
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if get_user_model().objects.filter(username=username).exists():
            return Response({"error":"이미 존재하는 사용자명입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if get_user_model().objects.filter(email=email).exists():
            return Response({"error":"이미 존재하는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
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
    

class UserPageAPIView(APIView):
    def get(self, request, username):
        pass