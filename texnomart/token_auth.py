from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User does not exist!"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user = User.objects.get(username=request.data['username'])
                token, _ = Token.objects.get_or_create(user=user)
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                    'token': token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
