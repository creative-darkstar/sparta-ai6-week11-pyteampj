from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, OtherUserSerializer


class SignupAPIView(APIView):
    def post(self, request):
        data = request.data

        username = data.get("username")
        email = data.get("email")

        # username, email 필수 입력 항목
        if not username or not email:
            return Response(
                {
                    "message":"필수 항목을 입력하여 주십시오."
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # username 중복 확인
        if get_user_model().objects.filter(username=username).exists():
            return Response({"error":"이미 존재하는 사용자명입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # email 중복 확인
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
        user = get_object_or_404(get_user_model(), username=username)

        if request.user == user:
            serializer = UserSerializer(user)
        else:
            serializer = OtherUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)

        # 해당 유저일 때만 수정 가능
        if request.user != user:
            return Response({"error":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # 소개, 비밀번호만 수정 가능
        user.introduction = request.data.get("introduction", user.introduction)
        user.password = request.data.get("password", user.password)

        # 비밀번호 빈칸 제출 불가
        if not user.password:
            return Response({"message":"비밀번호를 입력해 주십시오."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(user.password)
        # TODO 비밀번호 입력 확인, 비밀번호 조건 확인 
        user.save()
        return Response(status=status.HTTP_200_OK)
