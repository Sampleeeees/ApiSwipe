from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=70)
    surname = serializers.CharField(max_length=70)
    username = None

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.surname = self.validated_data.get('surname', '')
        user.role_id = 1
        user.save()

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'name': self.validated_data.get('name', ''),
            'surname': self.validated_data.get('surname', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', '')
        }

class CustomRegularUserRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=70)
    surname = serializers.CharField(max_length=70)
    username = None

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.surname = self.validated_data.get('surname', '')
        user.role_id = 2
        user.save()

    def get_cleaned_data(self):
        super(CustomRegularUserRegisterSerializer, self).get_cleaned_data()
        return {
            'name': self.validated_data.get('name', ''),
            'surname': self.validated_data.get('surname', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', '')
        }


class UserLoginSerializer(LoginSerializer):
    email = serializers.EmailField()
    username = None

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

