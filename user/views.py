from allauth.account import app_settings
from django.shortcuts import render
from allauth.account.views import ConfirmEmailView
from django.views.generic.base import TemplateResponseMixin, View
from dj_rest_auth.registration.views import RegisterView
from drf_spectacular.utils import extend_schema, extend_schema_view
from allauth.account.views import PasswordResetView
from .serializers import CustomRegisterSerializer, CustomRegularUserRegisterSerializer
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

@extend_schema(summary='Реєстрація забудовника', description='Для реєстрації потрібно вказати ваш актуальний email, пароль, повторити парооль, ваше імя та прізвище')
class BuilderRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

@extend_schema(summary='Реєстрація звичайного користувача', description='Для реєстрації потрібно вказати ваш актуальний email, пароль, повторити парооль, ваше імя та прізвище')
class UserRegisterView(RegisterView):
    serializer_class = CustomRegularUserRegisterSerializer


class ConfirmCustomEmailView(TemplateResponseMixin, View):
    """
        Template for send custom confirm password on email
        """
    template_name = 'account/email/confirm_verify_email.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'domain': get_current_site(self.request).domain})



class CustomPasswordResetView(PasswordResetView):
    """
    Template for send custom reset password on email
    """
    template_name = 'account/email/password_reset_confirm.html'

    @extend_schema(
        request={'type': 'object', 'properties': {'email': {'type': 'string'}}},
        responses={200: None}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
