from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .serializers import *
from rest_framework import  response, status, generics, viewsets
from drf_psq import PsqMixin, Rule
from user.permissions import *

@extend_schema(tags=['Image'])
class ImageViewSet(PsqMixin, generics.DestroyAPIView, generics.ListAPIView, viewsets.GenericViewSet):
    """
    ViewSet для обробки методів моделі Image
    """
    serializer_class = ImageListSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete', 'get']
    psq_rules = {
        ('destroy', 'list'): [
            Rule([IsAdminPermission | IsManagerPermission])
        ],
        ('house_delete', 'flat_delete'): [
            Rule([IsAdminPermission | IsOwnerPermission | CustomIsAuthenticate])
        ]
    }



    def get_object(self, *args, **kwargs):
        try:
            return Image.objects.select_related('gallery__house',
                                                'gallery__flat')\
                .get(pk=self.kwargs.get(self.lookup_field))
        except Image.DoesNotExist:
            raise ValidationError({'detail': _('Фото не знайдено')})

    def image_delete(self):
        obj = self.get_object()
        obj.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(summary='Список всіх зображень',
                   description='Цей endpoint дозволяє переглянути всі зображення що є на сайті. '
                               'Для цього потрібно бути авторизованим користувачем з правами Адміністратора')
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


    @extend_schema(summary='Видалення фото з системи',
                   description='Цей endpoint дозволяє видалити фото з системи. '
                               'Для цього ви повинні бути авторизованим користувачем в системі з правами Адміністратора')
    def destroy(self, request, *args, **kwargs):
        return self.image_delete()

    @extend_schema(summary='Видалення фото з будинку',
                   description='Цей endpoint дозволяє видалити фото з будинку. '
                               'Для цього ви повинні бути авторизованим користувачем в системі з правами Адміністратора')
    @action(methods=['DELETE'], detail=True, url_path='house/delete')
    def house_delete(self, request, *args, **kwargs):
        return self.image_delete()

    @extend_schema(summary='Видалення фото з квартири',
                   description='Цей endpoint дозволяє видалити фото з квартири. '
                               'Для цього ви повинні бути авторизованим користувачем в системі з правами Адміністратора')
    @action(methods=['DELETE'], detail=True, url_path='flat/delete')
    def flat_delete(self, request, *args, **kwargs):
        return self.image_delete()