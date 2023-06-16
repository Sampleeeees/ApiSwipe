from django.shortcuts import render
from drf_psq import PsqMixin, Rule
from drf_spectacular.utils import extend_schema
from rest_framework import status, response, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from flat.serializers import *
from user.permissions import CustomIsAuthenticate, IsAdminPermission, IsBuilderPermission, IsManagerPermission
from django.utils.translation import gettext_lazy as _

# Create your views here.

@extend_schema(tags=['Flats'])
class FlatView(PsqMixin, viewsets.ModelViewSet):
    parser_classes = [JSONParser]
    serializer_class = FlatApiSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    psq_rules = {
        'list': [
            Rule([CustomIsAuthenticate], FlatApiSerializer)
        ],
        'retrieve': [
            Rule([CustomIsAuthenticate])
        ],
        ('partial_update', 'destroy'): [
            Rule([IsAdminPermission]), Rule([IsManagerPermission])
        ],
        ('flat_user', 'flat_user_detail'): [
            Rule([IsBuilderPermission], FlatApiSerializer)
        ],
        ('create_flat_user', 'update_flat_user', 'delete_flat_user'): [
            Rule([IsBuilderPermission])
        ]
    }


    def get_object(self):
        try:
            return Flat.objects.get(pk=self.kwargs.get(self.lookup_field))
        except:
            raise ValidationError({'detail': _('Нет такой квартиры')})


    def get_queryset(self):
        queryset = Flat.objects \
            .prefetch_related('gallery__image_set') \
            .select_related('corps', 'section', 'floor', 'house', 'gallery') \
            .all()
        return queryset

    def get_user_obj(self):
        queryset = Flat.objects.filter(house__builder=self.request.user)
        return queryset

    def get_house(self):
        try:
            return House.objects.get(user=self.request.user)
        except:
            raise ValidationError({'detail': _('ЖК не зарегестрирован')})

    @action(methods=['GET'], detail=False, url_path='user')
    def flat_user(self, request, *args, **kwargs):
        obj = self.paginate_queryset(self.get_user_obj())
        serializer = self.get_serializer(instance=obj, many=True)
        return self.get_paginated_response(data=serializer.data)

    @action(methods=['GET'], detail=True, url_path='user/detail')
    def flat_user_detail(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj, many=False)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='user/create')
    def create_flat_user(self, request, *args, **kwargs):
        house = self.get_house()
        serializer = self.get_serializer(data=request.data, context={'house': house, 'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PATCH'], detail=True, url_path='user/update')
    def update_flat_user(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True, url_path='user/delete')
    def delete_flat_user(self, request, *args, **kwargs):
        obj = self.get_user_obj()
        obj.delete()
        return response.Response(data={'response': 'Obj удалён'}, status=status.HTTP_200_OK)