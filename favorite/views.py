from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import status, response, generics, viewsets
from rest_framework.decorators import action
from user.permissions import *
from .models import *
from .serializers import *
from django.utils.translation import gettext_lazy as _
# Create your views here.


@extend_schema(tags=['Favorite'])
class FavoriteViewSet(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    """
    ViewSet для обробки методів моделі Favorite
    """
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.filter(announcement__confirm=True)
    http_method_names = ['get', 'post', 'delete', 'patch']
    psq_rules = {
        'list': [
            Rule([CustomIsAuthenticate])
        ],
        'destroy': [
            Rule([IsAdminPermission | IsManagerPermission | IsBuilderPermission])
        ],
        ('favorite_user', 'favorite_user_update', 'favorite_user_delete'): [
            Rule([CustomIsAuthenticate])
        ]
    }

    def get_serializer_class(self):
        if self.action == 'favorite_user_update':
            return FavoriteUpdateSerializer
        return super().get_serializer_class()

    @extend_schema(summary='Список всіх збережених оголошень',
                   description='Цей endpoint дозволяє переглянути всі збережені оголошення що робили користувачі '
                               'на сайті. Ви повинні бути авторизованим користувачем з правами доступу Адміністратора')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення збережених оголошень',
                   description='Цей endpoint дозволяє видалити збережені оголошення'
                               '. Ви повинні бути авторизованим користувачем з правами доступу Адміністратора')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @extend_schema(summary='Список всіх збережених оголошень користувача',
                   description='Цей endpoint дозволяє переглянути всі збережені оголошення що робив користувач '
                               'на сайті. Ви повинні бути авторизованим користувачем')
    @action(methods=['GET'], detail=False, url_path='user')
    def favorite_user(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(user=request.user))
        if obj:
            serializer = self.get_serializer(instance=obj, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data={'detail': _('У вас немає улюблених оголошень')}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary='Створення збережених оголошень користувача',
                   description='Цей endpoint дозволяє створити збережені оголошення'
                               '. Ви повинні бути авторизованим користувачем')
    @action(methods=['POST'], detail=False, url_path='user/create')
    def favorite_user_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data={'message': _('Успішно створено'), 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return response.Response(data={'message': _('Помилка'), 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Видалення збережених оголошень користувача',
                   description='Цей endpoint дозволяє видалити збережені оголошення користувача'
                               '. Ви повинні бути авторизованим користувачем')
    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def favorite_user_delete(self, request, *args, **kwargs):
        if self.get_queryset().filter(user=request.user):
            obj = self.get_queryset().filter(pk=self.kwargs['pk'], user=request.user)
            if obj:
                obj.delete()
                return response.Response(data={'detail': _('Успішно видалено')}, status=status.HTTP_200_OK)
            else:
                return response.Response(data={'detail': _('Не вірно вказано id')}, status=status.HTTP_404_NOT_FOUND)
        else:
            return response.Response(data={'detail': _('У вас немає улюблених оголошень')}, status=status.HTTP_404_NOT_FOUND)