from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from house.paginators import PageNumberPagination
from announcement.models import Announcement
from .serializers import *
from drf_psq import PsqMixin, Rule
from rest_framework import viewsets, generics, response, status
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from user.permissions import IsAdminPermission, IsManagerPermission, IsBuilderPermission, CustomIsAuthenticate, IsOwnerPermission

# Create your views here.
@extend_schema(tags=['Announcement'])
class AnnouncementViewSet(PsqMixin, generics.ListAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    """
    ViewSet для обробки моделі Announcement з певними методами
    """
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all().order_by('id')
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [AllowAny]
    psq_rules = {
        'patch': [
            Rule([IsBuilderPermission, IsAdminPermission], AnnouncementBaseSerializer)
        ],
        ('announcement', 'user_update_announcement', 'user_delete_announcement'): [
            Rule([CustomIsAuthenticate], AnnouncementBaseSerializer)
        ]
    }

    def get_object(self, *args, **kwargs):
        try:
            return Announcement.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Announcement.DoesNotExist:
            return ValidationError({'detail': _('Такого оголошення не існує')})

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AnnouncementBaseSerializer
        return super().get_serializer_class()

    @extend_schema(summary='Список оголошень',
                   description='Цей endpoint дозволяє подивитися всі списки оголошень що є в системі')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретне оголошення',
                   description='Цей  endpoint дозволяє переглянути повну інформацію про конкретне оголошення.')
    def retrieve(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(instance=obj)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return response.Response(data={'detail': 'Такого оголошення не існує'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Часткове оновлення оголошення',
                   description='Цей endpoint дозволяє зробити часткове оновлення оголошення по id')
    def partial_update(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(data={'message': 'Дані оновленно', 'detail': serializer.data},
                                         status=status.HTTP_200_OK)
            else:
                return response.Response(data={'flat': _('Вказано невірну квартиру')},
                                         status=status.HTTP_400_BAD_REQUEST)
        except:
            return response.Response(data={'announcement_id': _('Вкажіть вірний id оголошення')})

    @extend_schema(summary='Видалення оголошення',
                   description='Цей endpoint дозволяє видалити оголошення по id')
    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.delete()
            return response.Response(data={'detail': _('Видалено')}, status=status.HTTP_200_OK)
        except:
            return response.Response(data={'detail': 'Такого оголошення не існує'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Оголошення авторизованого користувача',
                   description='Цей endpoint дозволяє переглянути всі оголошення які є у користувача що авторизувався в системі')
    @action(methods=['GET'], detail=False, url_path='user')
    def announcement(self, request, *args, **kwargs):
        try:
            obj = self.paginate_queryset(self.get_queryset().filter(flat__user=request.user))
            serializer = self.get_serializer(instance=obj, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        except AttributeError:
            return response.Response(data={'detail': _('У вас немає оголошень')}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Оновлення оголошення авторизованого користувача',
                   description='Цей endpoint дозволяє оновити оголошення які є у авторизованого користувача')
    @action(methods=['PATCH'], detail=True, url_path='user/update')
    def user_update_announcement(self, request, *args, **kwargs):
        try:
            obj = self.get_object(flat_user=request.user)
            serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(data={'message': _('Оголошення змінено'), 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, Announcement.DoesNotExist):
            return response.Response(data={'detail': _('У вас немає оголошення під таким id')})

    @extend_schema(summary='Видалення оголошення авторизованого користувача',
                   description='Цей endpoint дозволяє видалити оголошення які є у авторизованого користувача')
    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def user_delete_announcement(self, request, *args, **kwargs):
        try:
            obj = self.get_queryset().get(flat__user=request.user, id=self.kwargs['pk'])
            obj.delete()
            return response.Response(data={'response': 'Оголошення видалено'}, status=status.HTTP_200_OK)
        except (AttributeError, Announcement.DoesNotExist):
            return response.Response(data={'detail': _('У вас немає оголошення під таким id')}, status=status.HTTP_400_BAD_REQUEST)

