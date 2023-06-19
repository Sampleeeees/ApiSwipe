from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework import response, status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .serializers import *
from .models import *
from user.permissions import *
# Create your views here.

@extend_schema(tags=['Chessboard'])
class ChessboardViewSet(PsqMixin, generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = ChessboardSerializer
    queryset = ChessBoard.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']
    psq_rules = {
        ('list', 'partial_update', 'destroy'): [
            Rule([IsAdminPermission | IsManagerPermission])
        ],
        'user_chessboard': [
            Rule([CustomIsAuthenticate])
        ]
    }
    
    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ChessboardUpdateSerializer
        return super().get_serializer_class()

    @extend_schema(summary='Список шахматок',
                   description='Цей endpoint дозволяє переглянути всі шахматки що є в системі. '
                               'Для цього ви повинні бути авторизованим користувачем в системі з правами Адміністратора')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Часткове оновлення шахматки',
                   description='Цей endpoint дозволяє оновити шахматку що є в системі. '
                               'Для цього ви повинні бути авторизованим користувачем в системі з правами Адміністратора')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення шахматки',
                   description='Цей endpoint дозволяє видалити шахматку що є в системі. '
                               'Для цього ви повинні бути авторизованим користувачем в системі з правами Адміністратора')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @extend_schema(summary='Список всіх шахматок користувача',
                   description='Цей endpoint дозволяє переглянути всі шахматки що є у користувача')
    @action(methods=['GET'], detail=False, url_path='user/list')
    def user_chessboard(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(flat__user_id=self.request.user.id)
        if obj:
            serializer = self.get_serializer(instance=obj, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data={'detail': _('У вас немає шахматок')}, status=status.HTTP_400_BAD_REQUEST)