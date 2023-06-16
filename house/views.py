from django.shortcuts import render
from drf_psq import Rule, PsqMixin
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, generics, decorators, status, response
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .serializers import House64Serializer, HouseSerializer, FloorApiSerializer, SectionApiSerializer, CorpsApiSerializer, DocumentApiSerializer, NewsApiSerializer
from rest_framework.parsers import JSONParser, MultiPartParser
from .exceptions import CustomExceptionIsAuthenticated
from .paginators import CustomPagination
from .models import House
from user.permissions import *
# Create your views here.

@extend_schema(tags=['House'],)
class HouseViewSet(PsqMixin, viewsets.ModelViewSet):
    serializer_class = House64Serializer
    parser_classes = [JSONParser, MultiPartParser]
    permission_classes = [CustomIsAuthenticate]
    http_method_names = ['get', 'post', 'delete', 'patch']
    psq_rules = {
        'list': [
            Rule([CustomIsAuthenticate])
        ],
        'retrieve': [
            Rule([CustomIsAuthenticate])
        ],
        'create': [
            Rule([IsBuilderPermission])
        ],
        'destroy': [
            Rule([IsAdminPermission]),
            Rule([IsBuilderPermission])
        ],
        'partial_update': [
            Rule([IsBuilderPermission])
        ],
        'res_user': [
            Rule([IsBuilderPermission])
        ],
        ('update_res_user', 'delete_res_user'): [
            Rule([IsBuilderPermission])
        ]
    }

    @extend_schema(summary='Список будинків',
                   description='Ви можете отримати інформацію про всі будинки які створенні на сайті. '
                               'Але повинні бути авторизованим користувачем в системі')
    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return CustomExceptionIsAuthenticated
        return super().list(request, *args, *kwargs)

    @extend_schema(summary='Створити будинок',
                   description='Цей endpoint дозволяє авторизованому забудовнику створити будинок в системі.')
    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    @extend_schema(summary='Вивести інформацію про конкретний будинок',
                   description='Цей endpoint дозволяє подивитися повну інформацію про конкретний будинок. '
                               'Для цього ви повинні бути авторизовнаим в системі та знати id будинку.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення конкретного будинку',
                   description='Цей endpoint дозволяє видалити конкретний будинок по id.'
                               'Але для цього ви повинні бути авторизованим забудовником в системі')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @extend_schema(summary='Для частичного оновлення будинку',
                   description='Цей endpoint дозволяє оновити тільки те що вам потрібно. '
                               'Ви повинні бути авторизованим забудовником в системі')
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(self, request, *args, **kwargs)


    def serializer_choose(self, request):
        content_type = request.content_type
        if 'application/json' in content_type:
            return House64Serializer
        elif 'multipart/form-data' in content_type:
            return HouseSerializer

    def get_queryset(self):
        queryset = House.objects.prefetch_related('gallery__image_set').select_related('builder').all()
        return queryset

    def builder_obj(self):
        try:
            obj = House.objects.prefetch_related('gallery__image_set').select_related('builder').get(builder_id=self.request.user)
        except:
            return response.Response(data={'data': 'для забудовника не зареєстрований цей ЖК'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Інформація про авторизованого забудовника',
                   description='У цьому endpoint Ви можете глянути повну інформацію про забудовника.')
    @decorators.action(methods=['GET'], detail=True, url_path='builder')
    def res_user(self, request, *args, **kwargs):
        obj = self.builder_obj()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Оновлення часткової інформації про авторизованого забудовника',
                   description='Цей endpoint дозволяє частково оновити інформацію про забудовника. '
                               'Ви повинні бути авторизованим забудовником щоб могли оновити свої дані')
    @decorators.action(methods=['PATCH'], detail=True, url_path='builder/update')
    def update_res_user(self, request, *args, **kwargs):

        obj = self.builder_obj()

        serializer = self.serializer_choose(request)(data=request.data, instance=obj, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(summary='Видалення авторизованого забудовника ',
                   description='Цей endpoint дозволяє видалити забудовника з системи. '
                               'Потрібно бути авторизованим забудовником в системі щоб видалити самого себе')
    @decorators.action(methods=['DELETE'], detail=True, url_path='builder/delete')
    def delete_res_user(self, request, *args, **kwargs):
        obj = self.builder_obj()
        obj.delete()
        return response.Response(data={'response': 'Будинок видалено'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Floor'])
class FloorViewSet(PsqMixin, generics.RetrieveDestroyAPIView, generics.ListAPIView, viewsets.GenericViewSet):
    serializer_class = FloorApiSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Floor.objects.all()

    psq_rules = {
        'list': [
            Rule([CustomIsAuthenticate])
        ],
        ('update', 'destroy', 'create'): [
            Rule([IsBuilderPermission])
        ],
        'retrieve': [
            Rule([CustomIsAuthenticate])
        ],
        ('floor', 'create_floor', 'destroy_floor'): [
            Rule([IsBuilderPermission])
        ]
    }

    @extend_schema(summary='Список поверхів')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення поверху по id')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)


    def get_object(self, *args, **kwargs):
        try:
            return Floor.objects.get(pk=self.kwargs.get(self.lookup_field))
        except Floor.DoesNotExist:
            raise ValidationError({'detail': _('Такого поверху не існує.')})


    def get_house(self):
        try:
            return House.objects.get(builder=self.request.user)
        except:
            raise ValidationError({'detail': _('Будинок не створений')})

    @extend_schema(summary='Інформація про конкретний поверх')
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Список поверхів для забудовника',
                   description='Цей endpoint дозволяє дивитись поверхи для забудовника. '
                                   'Для цього потрібно бути авторизованим забудовником в системі')
    @decorators.action(methods=['GET'], detail=True, url_path='user')
    def floor(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_queryset().filter(house__builder=self.request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @extend_schema(summary='Створення поверху для забдовника',
                   description='Цей endpoint дозволяє створити поверх для забудовника. '
                               'Для цього потрібно бути авторизованим забудовником в системі')
    @decorators.action(methods=['POST'], detail=False, url_path='builder/create')
    def create_floor(self, request, *args, **kwargs):
        house = self.get_house()
        serializer = self.get_serializer(data=request.data, context={'house': house, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='Видалення поверху для забудовника',
                   description='Цей endpoint дозволяє видалити забудовнику поверх з його будинку. '
                               'Для цього потрібно бути авторизованим в системі та забудовником')
    @decorators.action(methods=['DELETE'], detail=True, url_path='builder/delete')
    def destroy_floor(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(house__builder=request.user)
        obj.delete()
        return response.Response(data={'response': 'Поверх видалено'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Section'])
class SectionViewSet(PsqMixin, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    serializer_class = SectionApiSerializer
    queryset = Section.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']
    psq_rules = {
        ('list', 'retrieve'): [
            Rule([CustomIsAuthenticate])
        ],
        ('create', 'partial_update', 'section', 'section_create', 'section_destroy'): [
            Rule([IsBuilderPermission])
        ],
    }


    def get_object(self, *args, **kwargs):
        try:
            obj = Section.objects.get(self.kwargs.get(self.lookup_field))
        except Section.DoesNotExist:
            return response.Response(data={'response': _('Такої секції не знайдено')})

    def get_house(self):
        try:
            House.objects.get(builder=self.request.user)
        except House.DoesNotExist:
            return ValidationError({'detail': _('Такого будинку не існує')})

    @extend_schema(summary='Список всіх секцій',
                   description='Цей endpoint дозволяє подивитися всі секції що є в системі. '
                               'Для цього ви повинні бути авторизованими')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Створення секції',
                   description='Цей endpoint дозволяє забудовнику створити секції для будинку. '
                               'Для цього ви повинні бути авторизованим забудовником в системі')
    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретну секцію',
                   description='Цей endpoint дозволяє подивитися всю інформацію про конкретну секцію. '
                               'Для цього ви повинні бути авторизованим в системі')
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Часткове оновлення секції')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення секції',
                   description='Цей endpoint дозволяє видалити секцію із системи. '
                               'Ви повинні бути авторизованим в системі забудовником.')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @decorators.action(methods=['GET'], detail=True, url_path='builder')
    def section(self):
        obj = self.paginate_queryset(self.get_queryset().filter(builder__house=self.request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)


    @decorators.action(methods=['POST'], detail=True, url_path='builder/create')
    def section_create(self, request, *args, **kwargs):
        house = self.get_house()
        serializer = self.get_serializer(data=request.data, context={'house': house, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @decorators.action(methods=['DELETE'], detail=True, url_path='builder/update')
    def section_destroy(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(house__builder=request.user)
        obj.delete()
        return response.Response(data={'response': 'Секцію видалено'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Corps'])
class CorpsViewSet(PsqMixin, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    serializer_class = CorpsApiSerializer
    queryset = Corps.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']
    psq_rules = {
        ('list', 'retrieve'): [
            Rule([CustomIsAuthenticate])
        ],
        ('create', 'partial_update', 'corps', 'corps_create', 'corps_destroy'): [
            Rule([IsBuilderPermission])
        ],
    }


    def get_object(self, *args, **kwargs):
        try:
            obj = Corps.objects.get(self.kwargs.get(self.lookup_field))
        except Corps.DoesNotExist:
            return response.Response(data={'response': _('Такого корпусу не знайдено')})

    def get_house(self):
        try:
            House.objects.get(builder=self.request.user)
        except House.DoesNotExist:
            return ValidationError({'detail': _('Такого будинку не існує')})

    @extend_schema(summary='Список всіх корпусів',
                   description='Цей endpoint дозволяє подивитися всі корпуси що є в системі. '
                               'Для цього ви повинні бути авторизованими')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Створення корпусу',
                   description='Цей endpoint дозволяє забудовнику створити корпус для будинку. '
                               'Для цього ви повинні бути авторизованим забудовником в системі')
    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретний корпус',
                   description='Цей endpoint дозволяє подивитися всю інформацію про конкретний корпус. '
                               'Для цього ви повинні бути авторизованим в системі')
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Часткове оновлення корпусу')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення корпусу',
                   description='Цей endpoint дозволяє видалити корпус із системи. '
                               'Ви повинні бути авторизованим в системі забудовником.')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @decorators.action(methods=['GET'], detail=True, url_path='builder')
    def corps(self):
        obj = self.paginate_queryset(self.get_queryset().filter(builder__house=self.request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)


    @decorators.action(methods=['POST'], detail=True, url_path='builder/create')
    def corps_create(self, request, *args, **kwargs):
        house = self.get_house()
        serializer = self.get_serializer(data=request.data, context={'house': house, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @decorators.action(methods=['DELETE'], detail=True, url_path='builder/update')
    def corps_destroy(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(house__builder=request.user)
        obj.delete()
        return response.Response(data={'response': 'Секцію видалено'}, status=status.HTTP_200_OK)

@extend_schema(tags=['Document'])
class DocumentViewSet(PsqMixin, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    serializer_class = DocumentApiSerializer
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    http_method_names = ['get', 'post', 'delete', 'patch']
    psq_rules = {
        ('list', 'retrieve'): [
            Rule([CustomIsAuthenticate])
        ],
        ('create', 'partial_update', 'corps', 'corps_create', 'corps_destroy'): [
            Rule([IsBuilderPermission])
        ],
    }


    def get_object(self, *args, **kwargs):
        try:
            obj = Corps.objects.get(self.kwargs.get(self.lookup_field))
        except Corps.DoesNotExist:
            return response.Response(data={'response': _('Такого документу не знайдено')})

    def get_house(self):
        try:
            House.objects.get(builder=self.request.user)
        except House.DoesNotExist:
            return ValidationError({'detail': _('Такого будинку не існує')})

    @extend_schema(summary='Список всіх документів',
                   description='Цей endpoint дозволяє подивитися всі документи що є в системі. '
                               'Для цього ви повинні бути авторизованими')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Створення документу',
                   description='Цей endpoint дозволяє забудовнику створити документ для будинку. '
                               'Для цього ви повинні бути авторизованим забудовником в системі')
    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретний документ',
                   description='Цей endpoint дозволяє подивитися всю інформацію про конкретний документ. '
                               'Для цього ви повинні бути авторизованим в системі')
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Часткове оновлення корпусу')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення документу',
                   description='Цей endpoint дозволяє видалити документ із системи. '
                               'Ви повинні бути авторизованим в системі забудовником.')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @decorators.action(methods=['GET'], detail=True, url_path='builder')
    def document(self):
        obj = self.paginate_queryset(self.get_queryset().filter(builder__house=self.request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)


    @decorators.action(methods=['POST'], detail=True, url_path='builder/create')
    def document_create(self, request, *args, **kwargs):
        house = self.get_house()
        serializer = self.get_serializer(data=request.data, context={'house': house, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @decorators.action(methods=['DELETE'], detail=True, url_path='builder/update')
    def document_destroy(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(house__builder=request.user)
        obj.delete()
        return response.Response(data={'response': 'Документ видалено'}, status=status.HTTP_200_OK)


@extend_schema(tags=['News'])
class NewsViewSet(PsqMixin, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    serializer_class = NewsApiSerializer
    queryset = News.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'patch']
    psq_rules = {
        ('list', 'retrieve'): [
            Rule([CustomIsAuthenticate])
        ],
        ('create', 'destroy', 'partial_update', 'news', 'news_create', 'news_destroy'): [
            Rule([IsBuilderPermission])
        ],
    }


    def get_object(self, *args, **kwargs):
        try:
            obj = News.objects.get(self.kwargs.get(self.lookup_field))
        except News.DoesNotExist:
            return response.Response(data={'response': _('Такої новини не знайдено')})

    def get_house(self):
        try:
            House.objects.get(builder=self.request.user)
        except House.DoesNotExist:
            return ValidationError({'detail': _('Такого будинку не існує')})

    @extend_schema(summary='Список всіх новин',
                   description='Цей endpoint дозволяє подивитися всі новини що є в системі. '
                               'Для цього ви повинні бути авторизованими')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    @extend_schema(summary='Створення корпусу',
                   description='Цей endpoint дозволяє забудовнику створити новину для будинку. '
                               'Для цього ви повинні бути авторизованим забудовником в системі')
    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    @extend_schema(summary='Інформація про конкретну новину',
                   description='Цей endpoint дозволяє подивитися всю інформацію про конкретну новину. '
                               'Для цього ви повинні бути авторизованим в системі')
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary='Часткове оновлення новини')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)

    @extend_schema(summary='Видалення новини',
                   description='Цей endpoint дозволяє видалити новину із системи. '
                               'Ви повинні бути авторизованим в системі забудовником.')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @decorators.action(methods=['GET'], detail=True, url_path='builder')
    def news(self):
        obj = self.paginate_queryset(self.get_queryset().filter(builder__house=self.request.user))
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)


    @decorators.action(methods=['POST'], detail=True, url_path='builder/create')
    def news_create(self, request, *args, **kwargs):
        house = self.get_house()
        serializer = self.get_serializer(data=request.data, context={'house': house, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @decorators.action(methods=['DELETE'], detail=True, url_path='builder/update')
    def news_destroy(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(house__builder=request.user)
        obj.delete()
        return response.Response(data={'response': 'Новину видалено'}, status=status.HTTP_200_OK)






