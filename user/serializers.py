from datetime import timedelta

from allauth.account.models import EmailAddress
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from rest_framework.exceptions import ValidationError

from .models import *

class CustomRegisterSerializer(RegisterSerializer):
    """
    Кастомний сериалізатор для реєстрації
    """
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
    """
    Кастомний serializer для реєстрації звичайного користувача
    """
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
    """
    Serializer для авторизації
    """
    email = serializers.EmailField()
    username = None

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer для відобаження підпики користувача
    """
    class Meta:
        model = Subscription
        fields = '__all__'


    def validate(self, attrs):
        me = attrs.get('me', False)
        me_and_agent = attrs.get('me_and_agent', False)
        agent = attrs.get('agent', False)
        disabled = attrs.get('disabled', False)

        if sum([me, me_and_agent, agent, disabled]) > 1:
            raise ValidationError({'detail': _('Тільки одне поле може мати значення True')})

        user = self.context['request'].user

        if self.context['request'].method == 'POST':
            if user.subscription is not None:
                raise ValidationError({'detail': _('У вас вже є підписка')})

        if self.context['request'].method == 'PATCH' or self.context['request'].method == 'DELETE':
            subscription_id = self.instance.id
            exist_subscription = Subscription.objects.filter(user=user, id=subscription_id).exists()
            if not exist_subscription:
                raise ValidationError({'detail': _('У вас немає доступу до цієї підписки')})

        return attrs

class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про роль
    """

    class Meta:
        model = Role
        fields = ['name_role']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про користувача з повною інформацією про підписку та роль
    """
    subscription = SubscriptionSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'username', 'is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions']

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer для створення користувача за допомогою multipart
    """
    avatar = serializers.ImageField(allow_null=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        exclude = ['last_login', 'username', 'is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'sales_departament', 'agent', 'subscription']

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data, username=validated_data.get('email'))
        except:
            raise ValidationError({'detail': _('Не вірно вказані дані')})

        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)

        return user


class UserCreateApiSerializer(serializers.ModelSerializer):
    """
    Serializer для створення користувача за допомогою json
    """
    avatar = Base64ImageField(use_url=True, required=False)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        exclude = ['last_login', 'username', 'is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'sales_departament', 'agent', 'subscription']

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data, username=validated_data.get('email'))
        except:
            raise ValidationError({'detail': _('Не вірно вказані дані')})

        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
        return user



class UserBlacklistSerializer(serializers.ModelSerializer):
    """
    Serializer для блокування користувача
    """

    class Meta:
        model = User
        fields = ['blacklist']

    def validate(self, attrs):
        boolean = attrs.get('blacklist', True)
        print(boolean)

        if not boolean:
            raise ValidationError({'detail': _('Значення може бути тільки true якщо ви зібралися заблокувати користувача')})

        return attrs

class UserUnBlacklistSerializer(serializers.ModelSerializer):
    """
    Serializer для розблокувння користувача
    """

    class Meta:
        model = User
        fields = ['blacklist']

    def validate(self, attrs):
        boolean = attrs.get('blacklist', False)

        if boolean:
            raise ValidationError({'detail': _('Значення може бути тільки false якщо ви зібралися розблокувати користувача')})

        return attrs

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про профіль користувача
    """
    avatar = Base64ImageField(use_url=True, required=False)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), allow_null=True, allow_empty=True, required=False)


    class Meta:
        model = User
        exclude = ['last_login', 'username', 'is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'sales_departament', 'agent', 'subscription', 'email']



class NotaryApiSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу нотаріусів з методом multipart
    """
    avatar = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'avatar', 'name', 'surname', 'phone_number', 'email']

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data, username=validated_data.get('email'))
        except:
            raise ValidationError({'detail': _('Не вірно вказані дані')})

        EmailAddress.objects.create(
            email=user.email,
            verified=True,
            primary=True,
            user=user
        )
        return user

    def validate(self, attrs):
        instance = self.instance
        if instance is not None:
            attrs.setdefault('avatar', instance.avatar)
            attrs.setdefault('email', instance.email)
        else:
            avatar = attrs.get('avatar')
            email = attrs.get('email')

            if not avatar:
                request = self.context.get('request')
                if request:
                    user = request.user
                    attrs['avatar'] = user.avatar

            if not email:
                attrs['email'] = attrs.get('email') or instance.email if instance else None

        return attrs

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance



class NotarySerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про нотаріусів з методом json
    """
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ['id', 'avatar', 'name', 'surname', 'phone_number', 'email']

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data, username=validated_data.get('email'))
        except:
            raise ValidationError({'detail': _('Не вірно вказані дані')})

        EmailAddress.objects.create(
            email=user.email,
            verified=True,
            primary=True,
            user=user
        )

        return user

class NotaryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних про користувача з правами Notary
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'phone_number']










