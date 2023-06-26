from rest_framework.test import APIClient
import pytest
from rest_framework_simplejwt.tokens import AccessToken

from user.models import User,Role


@pytest.fixture
def client():
    admin = User.objects.create(
        username='admin',
        email='admin@admin.com',
        password='admin123',
        is_superuser=True,
        role=Role.objects.create(is_admin=True)
    )
    client = APIClient()
    token = AccessToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
    return client

@pytest.fixture()
def builder():
    builder = User.objects.create(name='builder', surname='builder', email='builder@builder.com', role=Role.objects.create(is_builder=True))
    builder.set_password('swipe123')
    builder.save()
    client = APIClient()
    token = AccessToken.for_user(builder)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
    return client
