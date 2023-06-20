import base64
import io
import json
from PIL import Image as im
from rest_framework import serializers, status
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import *
from gallery.serializers import ImageSerializer
from gallery.models import Gallery, Image


def convert_base64_to_image(base64_string):
    """
    Функція для переробки зображення з Base64 в звичайний file для збереження фото
    """
    base64_data = base64_string.split(",")[1]
    image_data = base64.b64decode(base64_data)
    image_stream = io.BytesIO(image_data)
    image = im.open(image_stream)
    image_file = InMemoryUploadedFile(
        image_stream,
        None,
        'image.png',
        'image/png',
        image.tell(),
        None
    )

    return image_file

class HouseListSerializer(serializers.ModelSerializer):
    """
    Serializer для опису моделі House
    """
    class Meta:
        model = House
        fields = ['id', 'name']

    def to_internal_value(self, data: int) -> House:
        try:
            return House.objects.get(id=data['name'])
        except:
            raise ValidationError({'detail': _("Такого будинку не існує")})


class HouseSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних моделі House з multipart/form-data
    """
    general_image = serializers.ImageField()
    gallery_image = ImageSerializer(required=False, many=True)
    builder = serializers.HiddenField(default=serializers.CurrentUserDefault())
    address = serializers.CharField(allow_blank=True)
    map_position = serializers.CharField(allow_blank=True)
    min_price = serializers.IntegerField(default=0)
    price_for_m2 = serializers.IntegerField(default=0)
    area = serializers.IntegerField(default=0)
    description = serializers.CharField(allow_blank=True)
    sea_distance = serializers.IntegerField(default=0)

    class Meta:
        model = House
        exclude = ['gallery']
        extra_kwargs = {
            'builder': {'write_only': True}
        }

    def create(self, validated_data):
        gallery = self.context['request'].data.get('gallery_image', [])
        if not House.objects.filter(builder=self.context['request'].user).exists():
            created_house = House.objects.create(builder_id=self.context['request'].user.id,
                                                 gallery=Gallery.objects.create(text='house_gallery'),
                                                 **validated_data)
        else:
            raise ValidationError(detail={'data': _('Такий користувач вже має будинок')}, code=status.HTTP_400_BAD_REQUEST)

        if gallery:
            new_gallery = "[" + gallery + "]"
            for item in json.loads(new_gallery):
                print('item', item)
                image = Image.objects.create(image=convert_base64_to_image(item['image']),
                                             gallery=created_house.gallery)
                image.save()

        return created_house

    def update(self, instance: House, validated_data):
        gallery = self.context['request'].data.get('gallery_image', [])
        print('GALLERY', gallery)
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        print(instance.gallery)

        try:
            if gallery:
                new_gallery = "[" + gallery + "]"
                old_image = Image.objects.filter(gallery=instance.gallery)
                for item in old_image:
                    item.delete()

                for item in json.loads(new_gallery):
                    image = Image.objects.create(image=convert_base64_to_image(item['image']),
                                                 gallery=instance.gallery)
                    image.save()
        except:
            return ValidationError({'detail': _('Помилка при запису фото в галерею')})

        return instance



    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        data.update({
            'image': ImageSerializer(instance=instance.gallery.image_set.all(), many=True).data,
        })
        return data

class House64Serializer(serializers.ModelSerializer):
    """
    Serializer для опису даних моделі House з json
    """
    general_image = Base64ImageField()
    gallery_image = ImageSerializer(many=True, required=False)
    builder = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = House
        exclude = ['gallery']
        extra_kwargs = {
            'builder': {'write_only': True}
        }

    def create(self, validated_data):
        print(validated_data)
        gallery = validated_data.pop('gallery_image', None)
        if not House.objects.filter(builder=self.context['request'].user).exists():
            created_house = House.objects.create(builder_id=self.context['request'].user.id,
                                                 gallery=Gallery.objects.create(text='house_gallery'),
                                                 **validated_data)
        else:
            raise ValidationError(detail={'data': _('Такий користувач вже має будинок')}, code=status.HTTP_400_BAD_REQUEST)

        if gallery:
            for item in gallery:
                print('item', item)
                image = Image.objects.create(image=item.get('image'),
                                             gallery=created_house.gallery)
                image.save()
        return created_house

    def update(self, instance: House, validated_data):
        print(validated_data)
        gallery = validated_data.pop('gallery_image', None)

        for item in validated_data.keys():
            if validated_data.get(item):
                setattr(instance, item, validated_data.get(item))

        instance.save()

        try:
            if gallery:
                old_image = Image.objects.filter(gallery=instance.gallery)
                for item in old_image:
                    item.delete()

                for item in gallery:
                    image = Image.objects.create(image=item.get('image'),
                                                 gallery=instance.gallery)
                    image.save()
        except:
            return instance

        return instance


    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        data.update({
            'image': ImageSerializer(instance=instance.gallery.image_set.all(), many=True).data,
        })
        return data


class SectionApiSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних про секцію
    """
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Section
        fields = '__all__'


class CorpsApiSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних про корпус
    """
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Corps
        fields = '__all__'


class FloorApiSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних про поверх
    """
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Floor
        fields = '__all__'


class DocumentApiSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних про документ
    """
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Document
        fields = '__all__'


class NewsApiSerializer(serializers.ModelSerializer):
    """
    Serializer Для опису даних про новину
    """
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = News
        fields = '__all__'