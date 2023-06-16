from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import User


class EmailAuthBackend(object):
    """
    Authenticate using e-mail account.
    """
    def authenticate(self, nickname=None, password=None):
        try:
            User = get_user_model()
            user = User.objects.get(email=nickname)

            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None