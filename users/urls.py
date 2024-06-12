from django.urls import path
from .api import UserRetrieveDestroyAPIView, TokenObtainAPIView, RegisterAPIView, ResetPasswordCodeApiView, \
    ResetPasswordCodeVerifyApiView, ResetPasswordApiView

api_urls = ([
                path('users/<int:pk>/', UserRetrieveDestroyAPIView.as_view(), name='user-retrieve-destroy'),
                path("login/", TokenObtainAPIView.as_view(), name="user-login"),
                path("register/", RegisterAPIView.as_view(), name="user-register"),
                path('generate-code', ResetPasswordCodeApiView.as_view(), name="generate code recover password"),
                path('validate-code', ResetPasswordCodeVerifyApiView.as_view(), name="validate recover code "),
                path('recover-password-code', ResetPasswordApiView.as_view(), name="recover password with code"),
            ], 'users')

urlpatterns = [

]
