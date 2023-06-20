from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from user.permissions import *
from .serializers import *
# Create your views here.

@extend_schema(tags=['Message'])
class MessageViewSer(PsqMixin, generics.ListAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    """
    ViewSet для повідомлень для обробки різних методів
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    http_method_names = ['get', 'delete', 'patch', 'post']
    psq_rules = {
        ('list', 'destroy'): [
            Rule([IsAdminPermission])
        ],
        ('message_user_delete', 'message_user_update', 'message'): [
            Rule([IsSenderPermission])
        ],
        'message_user_create': [
            Rule([CustomIsAuthenticate])
        ]
    }

    def get_serializer_class(self):
        if self.action == 'message_user_update':
            return MessageUpdateSerializer
        elif self.action == 'message_user_create':
            return MessageCreateSerializer
        return super().get_serializer_class()

    @extend_schema(summary='Список всіх повідомлень',
                   description='Цей endpoint дозволяє переглянути всі повідомлення що є в системі. '
                               'Ви повинні бути авторизованим користувачем з правами доступу адміністратора')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення конкретного повідомлення',
                   description='Цей endpoint довзволяє видалити повідомлення з системи. '
                               'Для цього ви повинні бути авторизованим користувачем з правами Адміністратора')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @extend_schema(summary='Список всіх повідомлень користувача',
                   description='Цей endpoint дозволяє подивитися авторизованому користувачеві всі повідолмлення'
                               ' які він надсилав')
    @action(methods=['GET'], detail=False, url_path='sender')
    def message(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(user_sender=request.user))
        if obj:
            serializer = self.get_serializer(instance=obj, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data={'detail': _('Ви не відправляли жодного повідомлення')}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary='Оновлення повідомлення користувача',
                   description='Цей endpoint дозволяє оновити відправлене повідомлення авторизованого користувача')
    @action(methods=['PATCH'], detail=True, url_path='sender/update')
    def message_user_update(self, request, *args, **kwargs):
        try:
            obj = self.get_queryset().get(pk=self.kwargs['pk'], user_sender=request.user)
            serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response({'message': _('Повідомлення оновлено'), 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Message.DoesNotExist:
            return response.Response(data={'detail': _('У вас немає повідомлення під таким id')}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary='Видалення повідомлення користувачеві',
                   description='Цей endpoint дозволяє видалити своє повідомлення авторизованому користувачу який '
                               'надсилав повідомлення')
    @action(methods=['DELETE'], detail=True, url_path='sender/delete')
    def message_user_delete(self, request, *args, **kwargs):
        if not request.user.blacklist:
            try:
                obj = self.get_queryset().get(pk=self.kwargs['pk'], user_sender=request.user)
                obj.delete()
                return response.Response(data={'detail': 'Ваше повідомлення видалено'}, status=status.HTTP_200_OK)
            except (AttributeError, Message.DoesNotExist):
                return response.Response(data={'detail': _('Вказано не вірно id повідомлення або ви не маєте його')}, status=status.HTTP_404_NOT_FOUND)
        else:
            return response.Response(data={'detail': _('Ви занесені до чорного списку і не можете видаляти повідомлення')}, status=status.HTTP_423_LOCKED)

    @extend_schema(summary='Відправлення повідомлення',
                   description='Цей endpoint дозволяє відправити повідомлення в чат. Для цього вам потрібно бути '
                               'авторизованим користувачем в системі')
    @action(methods=['POST'], detail=False, url_path='sender/create')
    def message_user_create(self, request, *args, **kwargs):
        if not request.user.blacklist:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response.Response(data={'detail': _(f'Повідомлення відправленно у чат з id {serializer.data["chat"]}')}, status=status.HTTP_200_OK)
            else:
                return response.Response(data={'detail': _('Такого чату не існує')})
        else:
            return response.Response(data={'detail': _('Ви занесені до чорного списку і не можете відправляти повідомлення')}, status=status.HTTP_423_LOCKED)


@extend_schema(tags=['Chat'])
class ChatViewSet(PsqMixin, generics.ListAPIView, generics.RetrieveDestroyAPIView, viewsets.GenericViewSet):
    """
    ViewSet для чатів в яких адміністратор зможе робити різні операції
    """
    serializer_class = ChatContentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()
    http_method_names = ['get', 'delete']
    psq_rules = {
        ('list', 'destroy'): [
            Rule([IsAdminPermission])
        ],
        'retrieve': [
            Rule([IsAdminPermission | IsSenderPermission])
        ]
    }

    def get_object(self, *args, **kwargs):
        try:
            return Chat.objects.get(pk=self.kwargs['pk'])
        except Chat.DoesNotExist:
            return response.Response(data={'detail': _('Такого чату не знайдено')}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Список всіх чатів',
                   description='Цей endpoint дозволяє переглянути всі чати що є в системі. '
                               'Для цього потрібно бути авторизованим в системі та мати права Адміністратора')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретний чат',
                   description='Цей endpoint дозволяє переглянути чат та всі повідомлення що до нього посилаються. '
                               'Для цього потрібно бути авторизованим в системі та мати права Адміністратора або '
                               'відправника повідомлення')
    def retrieve(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = ChatMessageSerializer(instance=obj)
            return response.Response(data={'Chat': serializer.data}, status=status.HTTP_200_OK)
        except AttributeError:
            return response.Response(data={'detail': _('Не вірно вказано id чату')}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Видалення конкретного чату',
                   description='Цей endpoint дозволяє видалити конкретний чат по id. '
                               'Для цього ви повинні бути авторизованим та мати права Адміністратора')
    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.delete()
            return response.Response(data={'detail': 'Чат видалено'}, status=status.HTTP_200_OK)
        except AttributeError:
            return response.Response(data={'detail': _('Не вірно вказано id чату')})

