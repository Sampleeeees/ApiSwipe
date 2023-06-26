from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import response, status, viewsets, generics
from drf_psq import PsqMixin
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


# Create your views here.
@extend_schema(tags=['Promotion'])
class PromotionViewSet(PsqMixin, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    """
    ViewSet для обробки методів для моделі Promotion
    """
    serializer_class = PromotionSerializer
    queryset = Promotion.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']

    @extend_schema(summary='Список всіх просувань',
                   description='Цей endpoint дозволяє переглянути список всіх просувань. '
                               'Для цього ви повинні бути авторизованим в системі')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary='Створення просування',
                   description='Цей endpoint дозволяє створити просування. '
                               'Для цього ви повинні бути авторизованим в системі як адміністратор, менеджер,'
                               ' або власник')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретне просування',
                   description='Цей endpoint дозволяє переглянути інформацію про конкретне просування. '
                               'Для цього ви повинні бути авторизованим в системі')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary='Часткове оновлення просування',
                   description='Цей endpoint дозволяє частково або повністю оновити просування. '
                               'Для цього ви повинні бути авторизованим в системі як адміністратор, менеджер,'
                               ' чи власник')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(summary='Видалення просування',
                   description='Цей endpoint дозволяє видалити просування. '
                               'Для цього ви повинні бути авторизованим в системі як адміністратор, менеджер '
                               'або власник')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
