from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
# Create your models here.


class Role(models.Model):
    """
    Role which have any user
    """
    name_role = models.CharField(max_length=70, default='Regular user')
    is_regular = models.BooleanField(default=True)
    is_builder = models.BooleanField(default=False)
    is_notary = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


class Agent(models.Model):
    """
    Agent for regular user
    """
    name = models.CharField(max_length=70)
    surname = models.CharField(max_length=70)
    phone_number = models.IntegerField()
    email = models.EmailField()


class Subscription(models.Model):
    """
    Subscription for user
    """
    me = models.BooleanField()
    me_and_agent = models.BooleanField()
    agent = models.BooleanField()
    disabled = models.BooleanField()

class Sales_departament(models.Model):
    """
    Models for Sales Departament in User cabinet for Builder Role
    """
    name = models.CharField(max_length=70)
    surname = models.CharField(max_length=70)
    phone_number = models.IntegerField()
    email = models.EmailField()


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model abstract for custom User
    """
    username = models.CharField(max_length=70, blank=True, null=True)
    name = models.CharField(max_length=70, default='user', blank=True, null=True)
    surname = models.CharField(max_length=70, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField(unique=True)
    avatar = models.FileField(upload_to='user/avatar/', blank=True, null=True)
    switch_call_message = models.BooleanField(blank=True, null=True, default=False)
    blacklist = models.BooleanField(blank=True, null=True, default=False)
    agent = models.ForeignKey(Agent, verbose_name='Агент', null=True, blank=True, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, verbose_name='Підписка', null=True, blank=True, on_delete=models.CASCADE)
    sales_departament = models.ForeignKey(Sales_departament, verbose_name='Відділ кадрів', null=True, blank=True, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, verbose_name='Роль', null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


