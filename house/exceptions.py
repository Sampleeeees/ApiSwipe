from rest_framework.exceptions import NotAuthenticated
from django.utils.translation import gettext_lazy as _

class CustomExceptionIsAuthenticated(NotAuthenticated):
    default_detail = _('Ви повинні авторизуватися в системі')