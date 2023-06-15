from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # User 모델 생성
            user = User.objects.create(
                username=serializer.validated_data['username'],
                team=serializer.validated_data['team'],
                password=make_password(serializer.validated_data['password']),
                )  # 인증 번호 저장
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'message': '회원가입이 완료되었습니다.', 'token': access_token, 'refresh_token': refresh_token},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)