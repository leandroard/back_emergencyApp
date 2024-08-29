from rest_framework import serializers
from .models import User, EmergencyRoleModel, Role
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'number_id')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')  # Asume que Role tiene un campo 'name', ajusta según tu modelo

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'number_id', 'role')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'number_id', 'email', 'password')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): # noqa
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token["user"] = UserTokenSerializer(user, many=False).data
        return token

class EmergencyRoleSerializerRequest(serializers.Serializer):
    role = serializers.ChoiceField(choices=[role[0] for role in Role.ROLE_CHOICES])
    number_id = serializers.CharField(max_length=255, required=False)
    adress = serializers.CharField(max_length=255, required=False)
    plate_vehicle = serializers.CharField(max_length=255, required=False)


class EmeregencyRoleSerializerResponse(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmergencyRoleModel
        fields = ('id', 'user', 'status', 'role', 'plate_vehicle' )


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