from django.urls import path
from .api import UserRetrieveDestroyAPIView, TokenObtainAPIView, RegisterAPIView, ResetPasswordCodeApiView, \
    ResetPasswordCodeVerifyApiView, ResetPasswordApiView, CurrentUserAPIView, TokenRefreshAPIView, ChangeRoleAPIView, UserListAPIView, EmergencyRoleListAPIView

api_urls = ([
        path("current/", CurrentUserAPIView.as_view(), name="get-current-user"),
                path('users/<int:pk>/', UserRetrieveDestroyAPIView.as_view(), name='user-retrieve-destroy'),
                                path('users/', UserListAPIView.as_view(), name='user-retrieve-destroy'),
                path('postulations/', EmergencyRoleListAPIView.as_view(), name='user-retrieve-destroy'),

                path("login/", TokenObtainAPIView.as_view(), name="user-login"),
                path("register/", RegisterAPIView.as_view(), name="user-register"),
                path("refresh/", TokenRefreshAPIView.as_view(), name="user-refresh-token"),
                path("change-role/", ChangeRoleAPIView.as_view(), name="change-role"),
                path('generate-code', ResetPasswordCodeApiView.as_view(), name="generate code recover password"),
                path('validate-code', ResetPasswordCodeVerifyApiView.as_view(), name="validate recover code "),
                path('recover-password-code', ResetPasswordApiView.as_view(), name="recover password with code"),
            ], 'users')

urlpatterns = [

]
