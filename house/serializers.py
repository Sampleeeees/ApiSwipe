from rest_framework import serializers, status
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from django.utils.translation import gettext_lazy as _

from .models import *
from gallery.serializers import ImageSerializer
from gallery.models import Gallery, Image


class HouseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = House
        fields = ['id', 'name']

    def to_internal_value(self, data: int) -> House:
        try:
            return House.objects.get(id=data['name'])
        except:
            raise ValidationError({'detail': _("Такого будинку не існує")})


class HouseSerializer(serializers.ModelSerializer):

    general_image = serializers.ImageField()
    image = ImageSerializer(required=False, many=True)

    class Meta:
        model = House
        exclude = ['gallery']

    def create(self, validated_data):
        gallery = validated_data.pop('image', None)
        if not House.objects.filter(builder=self.context['request'].user):
            created_house = House.objects.create(builder=self.context['request'].user,
                                                 gallery = Gallery.objects.create(text='house_gallery'),
                                                 **validated_data)
        else:
            raise ValidationError(detail={'data': _('Такий користувач вже має будинок')}, code=status.HTTP_400_BAD_REQUEST)

        if gallery:
            for item in gallery:
                image = Image.objects.create(image=item.get('image'),
                                             gallery=created_house.gallery)
                image.save()
        return created_house

    def update(self, instance: House, validated_data):
        gallery = validated_data.pop('image', None)

        for item in validated_data.keys():
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

class House64Serializer(serializers.ModelSerializer):
    general_image = Base64ImageField()
    image = ImageSerializer(many=True, required=False)

    class Meta:
        model = House
        exclude = ['gallery']

    def create(self, validated_data):
        gallery = validated_data.pop('image', None)
        if not House.objects.filter(builder=self.context['request'].user):
            created_house = House.objects.create(builder=self.context['request'].user,
                                                 gallery = Gallery.objects.create(text='house_gallery'),
                                                 **validated_data)
        else:
            raise ValidationError(detail={'data': _('Такий користувач вже має будинок')}, code=status.HTTP_400_BAD_REQUEST)

        if gallery:
            for item in gallery:
                image = Image.objects.create(image=item.get('image'),
                                             gallery=created_house.gallery)
                image.save()
        return created_house

    def update(self, instance: House, validated_data):
        gallery = validated_data.pop('image', None)

        for item in validated_data.keys():
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
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Section
        fields = '__all__'


class CorpsApiSerializer(serializers.ModelSerializer):
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Corps
        fields = '__all__'


class FloorApiSerializer(serializers.ModelSerializer):
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Floor
        fields = '__all__'


class DocumentApiSerializer(serializers.ModelSerializer):
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = Document
        fields = '__all__'


class NewsApiSerializer(serializers.ModelSerializer):
    house = PrimaryKeyRelatedField(queryset=House.objects.all(), required=False)

    class Meta:
        model = News
        fields = '__all__'