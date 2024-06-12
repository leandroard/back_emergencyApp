from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): # noqa
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token["user"] = UserTokenSerializer(user, many=False).data
        return token


class TokenOutputSerializer(serializers.Serializer): # noqa
    refresh = serializers.CharField(label=_("Refresh token"))
    access = serializers.CharField(label=_("Access token"))

class ResetPasswordRequestSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField(required=True)


class ResetPasswordCodeValidateRequestSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()