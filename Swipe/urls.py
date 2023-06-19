"""Swipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from django.conf.urls.static import static
from Swipe import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from user.serializers import CustomRegisterSerializer
from allauth.account.views import ConfirmEmailView, PasswordResetDoneView
from drf_spectacular.utils import extend_schema
from user.views import BuilderRegisterView, UserRegisterView, ConfirmCustomEmailView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    # Spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Register new user or builder
    path('api/registration/builder', BuilderRegisterView.as_view(), name='register_builder'),
    path('api/registration/user', UserRegisterView.as_view(), name='account_signup'),
    # Confirm Email
    path('api/auth/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('api/auth/confirm-email-verify', ConfirmCustomEmailView.as_view(), name='confirm_verify_email'),
    path('api/auth/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/auth/login/', LoginView.as_view(), name='account_login'),
    path('api/auth/logout/', LogoutView.as_view(), name='account_logout'),
    path('api/auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('api/auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/auth/resend-email/', ResendEmailVerificationView.as_view(), name='account_resend_email'),
    path('api/auth/password-reset/confirm/<uidb64>/<token>/', PasswordResetDoneView.as_view(), name='password_reset_confirm'),
    # apps

    path('api/v1/', include('house.urls')),
    path('api/v1/', include('flat.urls')),
    path('api/v1/', include('announcement.urls')),
    path('api/v1/', include('message.urls')),
    path('api/v1/', include('filter.urls')),
    path('api/v1/', include('promotion.urls')),
    path('api/v1/', include('favorite.urls')),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('chessboard.urls')),
    path('api/v1/', include('gallery.urls'))


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
