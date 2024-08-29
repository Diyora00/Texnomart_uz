from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class LoginModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        refresh = RefreshToken.for_user(user)
        return {
            'username': user.username,
            'email': user.email,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', )
        password = attrs.get('password', )
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Bad credentials')
        if not user.is_active:
            raise AuthenticationFailed('User inactive or deleted')
        return attrs


class LoginAPIView(APIView):
    serializer_class = LoginModelSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)