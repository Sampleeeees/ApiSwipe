from allauth.account import app_settings
from django.shortcuts import render
from allauth.account.views import ConfirmEmailView
from django.views.generic.base import TemplateResponseMixin, View
from dj_rest_auth.registration.views import RegisterView
from drf_spectacular.utils import extend_schema, extend_schema_view
from allauth.account.views import PasswordResetView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .serializers import CustomRegisterSerializer, CustomRegularUserRegisterSerializer
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.sites.shortcuts import get_current_site
from drf_psq import PsqMixin
from rest_framework import response, status, generics, viewsets
from .models import *
from django.utils.translation import gettext_lazy as _
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

@extend_schema(tags=['Subscription'])
class SubscriptionViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(summary='Список всіх підписок',
                   description='Цей endpoint дозволяє переглянути всі підписки що є на сайті')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Створення підписки',
                   description='Цей endpoint дозволяє створити підписку. '
                               'Ви повинні бути звичайним користувачем та не мати вже підписки інакше '
                               'просто оновіть свою')
    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про підписку',
                   description='Цей endpoint дозволяє переглянути вашу підписку що є на сайті. '
                               'Для цього ви повинні бути звичайним користувачем та мати свою підписку')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @extend_schema(summary='Часткове оновлення підписки',
                   description='Цей endpoint дозволяє оновити підписку. '
                               'Для цього ви повинні бути звичайним користувачем та мати підписку')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення підписки',
                   description='Цей endpoint дозволяє видалити підписку')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

@extend_schema(tags=['User'])
class UserViewSet(PsqMixin, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    parser_classes = [JSONParser, MultiPartParser]
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def serializer_choose(self, request):
        content_type = request.content_type
        print(request.content_type)
        if 'application/json' in content_type:
            return UserCreateApiSerializer
        elif 'multipart/form-data' in content_type:
            return UserCreateSerializer
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return UserCreateApiSerializer
        if self.action == 'user_block':
            return UserBlacklistSerializer
        if self.action == 'user_unblock':
            return UserUnBlacklistSerializer
        if self.action == 'user_profile_update':
            return UserProfileUpdateSerializer
        return super().get_serializer_class()

    @extend_schema(summary='Список всіх користувачів',
                   description='Цей endpoint дозволяє переглянути всіх користувачів в системі. '
                               'Для цього ви повинні бути авторизованим користувачем з правами доступу Адміністратора')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про користувача',
                   description='Цей endpoint дозволяє переглянути інформацію про користувача в системі. '
                               'Для цього ви повинні бути авторизованим користувачем з правами доступу Адміністратора')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @extend_schema(summary='Створення користувача',
                   description='Цей endpoint дозволяє створити користувача в системі. '
                               'Для цього ви повинні бути авторизованим користувачем з правами доступу Адміністратора')
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_choose(request)(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data={'message': _('Користувача створено'), 'detail': serializer.data}, status=status.HTTP_201_CREATED)
        return response.Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Видалення користувача',
                   description='Цей endpoint дозволяє видалити користувача в системі. '
                               'Для цього ви повинні бути авторизованим користувачем з правами доступу Адміністратора')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @extend_schema(summary='Часткове оновлення користувача',
                   description='Цей endpoint дозволяє оновити інформацію про користувача в системі. '
                               'Для цього ви повинні бути авторизованим користувачем з правами доступу Адміністратора')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(summary='Чорний список',
                   description='Цей endpoint дозволяє переглянути всіх користувачів що знаходяться в чорному списку. '
                               'Дял цього ви повинні бути користувачем з правами доступу Адміністратора')
    @action(methods=['GET'], detail=False, url_path='user/blacklist')
    def user_blacklist(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(blacklist=True)
        if obj:
            serializer = self.get_serializer(instance=obj, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data={'detail': _('У Blacklist немає жодного користувача')})

    @extend_schema(summary='Профіль користувача',
                   description='Цей endpoint дозволяє переглянути опис профілю користувача що авторизований. '
                               'Для цього потрібно бути авторизованим в системі')
    @action(methods=['GET'], detail=False, url_path='profile')
    def user_profile(self, request, *args, **kwargs):
        obj = self.get_queryset().get(id=self.request.user.id)
        print(obj)
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Часткове оновлення профілю користувача',
                   description='Цей endpoint дозволяє частково оновити ваш профіль. '
                               'Для цього потрібно бути авторизованим в системі')
    @action(methods=['PATCH'], detail=False, url_path='profile/update')
    def user_profile_update(self, request, *args, **kwargs):
        obj = self.get_queryset().get(id=self.request.user.id)
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data={'message': _('Дані оновлено'), 'detail': serializer.data}, status=status.HTTP_200_OK)
        else:
            return response.Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Заблокувати користувача',
                   description='Цей endpoint дозволяє заблокувати користувача в системі. '
                               'Для цього ви повинні бути авторизовані в системі з правами Адміністратора')
    @action(methods=['POST'], detail=True, url_path='user/block')
    def user_block(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(blacklist=False)
        if queryset:
            try:
                obj = self.get_queryset().get(pk=self.kwargs['pk'])
                if not obj.blacklist:
                    serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return response.Response(data={'message': _('Користувача заблоковано'), 'detail': serializer.data}, status=status.HTTP_200_OK)
                    else:
                        return response.Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return response.Response(data={'detail': _('Користувач вже й так заблокований')}, status=status.HTTP_409_CONFLICT)
            except User.DoesNotExist:
                return response.Response(data={'detail': _('Користувача під таким id не знайдено')}, status=status.HTTP_404_NOT_FOUND)
        else:
            return response.Response(data={'detail': _('Усі користувачі вже й так заблоковані :)')}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Розблокувати користувача',
                   description='Цей endpoint дозволяє розблокувати користувача в системі. '
                               'Для цього ви повинні бути авторизовані в системі з правами Адміністратора')
    @action(methods=['POST'], detail=True, url_path='user/unblock')
    def user_unblock(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(blacklist=True)
        if queryset:
            try:
                obj = self.get_queryset().get(pk=self.kwargs['pk'])
                if obj.blacklist:
                    serializer = self.get_serializer(data=request.data, partial=True, instance=obj)
                    if serializer.is_valid():
                        serializer.save()
                        return response.Response(data={'message': _('Користувача розблоковано'), 'detail': serializer.data},
                                                 status=status.HTTP_200_OK)
                    else:
                        return response.Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return response.Response(data={'detail': _('Користувач вже й так розблокований')}, status=status.HTTP_409_CONFLICT)

            except User.DoesNotExist:
                return response.Response(data={'detail': _('Користувача під таким id не знайдено')})

        else:
            return response.Response(data={'detail': _('Усі користувачі вже й так розблоковані :)')})


@extend_schema(tags=['Notary'])
class NotaryViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = NotaryApiSerializer
    parser_classes = [JSONParser, MultiPartParser]
    queryset = User.objects.filter(role__is_notary=True)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def serializer_choose(self, request):
        content_type = request.content_type
        if 'application/json' in content_type:
            return NotaryApiSerializer
        elif 'multipart/form-data' in content_type:
            return NotarySerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return NotaryUpdateSerializer
        return super().get_serializer_class()

    @extend_schema(summary='Список всіх нотаріусів',
                   description='Цей endpoint дозволяє переглянути всіх нотаріусів в системі. '
                               'Для цього ви повинні бути авторизованим в системі з правами Адміністратора')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретний нотаріус',
                   description='Цей endpoint дозволяє переглянути інформацію про нотаріус в системі. '
                               'Для цього ви повинні бути авторизованим в системі з правами Адміністратора')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self ,request, *args, **kwargs)

    @extend_schema(summary='Видалення нотаріусу',
                   description='Цей endpoint дозволяє видалити нотаріус з системи. '
                               'Для цього ви повинні бути авторизованим в системі з правами Адміністратора')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @extend_schema(summary='Створення нотаріусу',
                   description='Цей endpoint дозволяє створити нотаріус в системі. '
                               'Для цього ви повинні бути авторизованим в системі з правами Адміністратора')
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_choose(request)(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data={'message': _('Створено'), 'detail': serializer.data}, status=status.HTTP_201_CREATED)
        return response.Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(summary='Часткове оновлення нотаріусу',
                   description='Цей endpoint дозволяє оновити нотаріус в системі. '
                               'Для цього ви повинні бути авторизованим в системі з правами Адміністратора')
    def partial_update(self, request, *args, **kwargs):
        obj = self.get_queryset().get(pk=self.kwargs['pk'])
        serializer = self.serializer_class(data=request.data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data={'message': _('Успішно оновлено'), 'data': serializer.data}, status=status.HTTP_206_PARTIAL_CONTENT)
        return response.Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)







