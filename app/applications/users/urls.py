from django.urls import path
from django_rest_passwordreset.urls import add_reset_password_urls_to_router
from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_validate_token,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from applications.users.views import (
    ChangePasswordView,
    CustomResetPasswordConfirm,
    LoginView,
    LogoutView,
    RegistrationView,
)

app_name = 'users'

router = DefaultRouter()
add_reset_password_urls_to_router(router, base_path='docs/forgot-password')

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),

    path('forgot-password/', reset_password_request_token, name='reset-password-request'),
    path('forgot-password/validate_token/', reset_password_validate_token, name='reset-password-validate'),
    path('forgot-password/confirm/', CustomResetPasswordConfirm.as_view(), name='reset-password-confirm'),

    path('token-refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls

# To refresh the access token, the refresh token needs to be sent to token-refresh using a POST request.
# More information can be found
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#usage
