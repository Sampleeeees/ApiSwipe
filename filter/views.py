from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets, response, status
from drf_psq import PsqMixin, Rule
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from user.permissions import *
from .serializers import *
# Create your views here.

@extend_schema(tags=['Filter'])
class FilterViewSet(PsqMixin, generics.ListAPIView, viewsets.GenericViewSet):
    """
    ViewSer для обробки методів моделі Filter
    """
    serializer_class = FilterSerializer
    queryset = Filter.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']
    psq_rules = {
        'list': [
            Rule([IsAdminPermission])
        ]
    }


    def get_serializer_class(self):
        if self.action == 'filter_user_create':
            return FilterSaveSerializer
        return super().get_serializer_class()


    def get_object(self, *args, **kwargs):
        try:
            return Filter.objects.get(pk=self.kwargs.get(self.lookup_field))
        except:
            return response.Response(data={'detail': 'Такого фільтру не збережено'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary='Список всіх фільтрів',
                   description='Цей endpoint дозволяє переглянути всі збережені фільтри та користувача який їх зберіг. '
                               'Для цього ви повинні бути авторизованим та мати права доступу Адміністратор')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Список всіх фільтрів користувача',
                   description='Цей endpoint дозволяє подивитися всі фільтри які зберігав авторизований користувач.  '
                               'Відповідно для цього ви повинні бути авторизованим в системі та мати хоча б один'
                               ' збережений фільтр')
    @action(methods=['GET'], detail=False, url_path='user')
    def filter(self, request, *args, **kwargs):
        try:
            obj = self.paginate_queryset(self.get_queryset().filter(user=request.user))
            serializer = self.get_serializer(instance=obj, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        except (AttributeError, Filter.DoesNotExist):
            return response.Response(data={'detail': _('Такого фільтру не збережено')}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Збереження фільру',
                   description='Цей endpoint дозволяє зберегти фільтр. '
                               'Для цього ви повинні бути авторизованим в системі')
    @action(methods=['POST'], detail=False, url_path='user/create')
    def filter_user_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data={'message': _('Успішно збережено'), 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return response.Response(data={'message': _('Не вдалось зберегти'), 'error': serializer.erorrs}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Видалення фільтру користувачем',
                   description='Цей endpoint дозволяє видалити фільтр по id тільки ті які він зберігав. '
                               'Для цього ви повинні бути авторизованим та мати збережені фільтри в системі')
    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def filter_user_delete(self, request, *args, **kwargs):
        filter_user = self.get_queryset().filter(user=request.user)
        if filter_user:
            obj = self.get_queryset().filter(pk=self.kwargs['pk'], user=request.user)
            if obj:
                obj.delete()
                return response.Response(data={'detail': _('Фільтр видалено')}, status=status.HTTP_200_OK)
            else:
                return response.Response(data={'detail': _('У вас немає фільтру під таким id')}, status=status.HTTP_404_NOT_FOUND)
        else:
            return response.Response(data={'detail': 'У вас немає збережених фільтрів'}, status=status.HTTP_400_BAD_REQUEST)

