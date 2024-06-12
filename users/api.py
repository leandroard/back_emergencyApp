from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, CodeRecoverPassword
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, UserCreateSerializer, CustomTokenObtainPairSerializer, TokenOutputSerializer, \
    ResetPasswordSerializer, ResetPasswordRequestSerializer, ResetPasswordCodeValidateRequestSerializer
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import datetime
import jwt
from .views import generate_code


@extend_schema(tags=['Users'])
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@extend_schema(tags=['Users'])
class UserRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=['Authenticate'])
class TokenObtainAPIView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        description=_("Iniciar Sesión"),
        responses={200: TokenOutputSerializer},
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(tags=['Authenticate'])
class RegisterAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary=_("Registrar un nuevo Usuario"),
        description=_("Registrar un nuevo Usuario"),
        request=UserCreateSerializer,
        responses={200: UserSerializer},
        methods=["post"]
    )
    def post(self, request, *args, **kwargs):
        """
        Register a new user and return it's details
        """
        try:
            User.objects.get(email=request.data["email"])
            return Response({'detail': _('Ya existe un usuario con este correo o nombre de usuario')}, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            email = request.data['email']
            # Generate a username value based in the email value
            #username = User.generate_username(email)

            user = User.objects.create_user(
                username="username",
                email=email,
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                password=request.data["password"],
            )
            return Response(UserSerializer(user, context={'request': request}).data)



class ResetPasswordCodeApiView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer


    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        email = request.data['email']
        if serializer.is_valid(raise_exception=False):
            try:
                user = User.objects.get(email=email)
                code = generate_code()
                expiration = timezone.now() + timedelta(minutes=60)
                code_recovery = CodeRecoverPassword.objects.create(
                    user_id=user,
                    code=code,
                    created=timezone.now(),
                    expiration=expiration
                )
                if code_recovery.pk:
                    subject = _("Restablecer Contraseña")
                    html_message = render_to_string('recover password/reset_password_code.html', {
                        'code': code,
                        'first_name': user.first_name,
                    })
                    send_email = send_mail(
                        subject, '',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                        html_message=html_message)
                    if send_email > 0:
                        return Response({"detail": _("Correo enviado")}, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': _('No se logro enviar el correo')},
                                        status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'detail': _('No existe un usuario con este correo')}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordCodeVerifyApiView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordCodeValidateRequestSerializer

    def post(self, request, *args, **kwargs):
        try:
            code_ = request.data['code']
            email = request.data['email']
            user = User.objects.get(email=email)
            code = CodeRecoverPassword.objects.get(code=code_, user_id=user)
            if code is not None:
                if code.expiration > timezone.now():
                    code.delete()
                    payload = {
                        'user_id': user.id,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(
                            days=settings.PASSWORD_RESET_EXPIRE_DAYS),
                        'iat': datetime.datetime.utcnow(),
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    return Response({'detail': 'Codigo valido', 'token': token}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'El codigo a caducado'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'El correo es invalido'}, status=status.HTTP_400_BAD_REQUEST)
        except CodeRecoverPassword.DoesNotExist:
            return Response({'detail': 'Codigo invalido'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApiView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            payload = jwt.decode(request.data['token'], settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            validate = password_validation.validate_password(request.data['password'])
            if validate:
                encrypted_password = make_password(request.data['password'])
                user.password = encrypted_password
                user.save()
            return Response({'detail': 'El cambio de contraseña a sido exitoso!'})
        except ValidationError as e:
            return Response({'detal': 'La contraseña debe ser mayor a 8 caracteres y contener como minimo una letra'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'El token a caducado'})
        except jwt.DecodeError:
            return Response({'detail': 'Error del token de seguridad'})
        except User.DoesNotExist:
            return Response({'detail': 'El usuario no se encontro'})
