from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from flat.models import Flat
from house.models import Section, Floor, Corps, House
from house.serializers import HouseListSerializer
from gallery.serializers import ImageSerializer
from gallery.models import Gallery, Image


class SectionFlatSerializer(serializers.ModelSerializer):
    """
    Serializer для секцій у якому є перевірка інсуючого значення секції
    """
    class Meta:
        model = Section
        fields = ['id', 'name']

    def to_internal_value(self, data: int):
        try:
            return Section.objects.select_related('house').get(pk=data['name'])
        except Section.DoesNotExist:
            raise ValidationError({'section': _('Секція не існує')})
        except (TypeError, IndexError):
            raise ValidationError({'section': _('Неправильно вказана секція')})


class CorpsFlatSerializer(serializers.ModelSerializer):
    """
    Serializer для секцій у якому є перевірка інсуючого значення корпусу
    """
    class Meta:
        model = Corps
        fields = ['id', 'name']

    def to_internal_value(self, data: int):
        try:
            return Corps.objects.select_related('house').get(pk=data['name'])
        except Corps.DoesNotExist:
            raise ValidationError({'corps': _('Корпус не існує')})
        except (TypeError, IndexError):
            raise ValidationError({'corps': _('Неправильно вказаний корпус')})


class FloorFlatSerializer(serializers.ModelSerializer):
    """
    Serializer для секцій у якому є перевірка інсуючого значення поверху
    """
    class Meta:
        model = Floor
        fields = ['id', 'name']

    def to_internal_value(self, data: int):
        try:
            return Floor.objects.select_related('house').get(pk=data['name'])
        except Floor.DoesNotExist:
            raise ValidationError({'floor': _('Поверху не існує')})
        except (TypeError, IndexError):
            raise ValidationError({'floor': _('Неправильно вказаний поверх')})


class FlatApiSerializer(serializers.ModelSerializer):
    house = serializers.PrimaryKeyRelatedField(queryset=House.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all())
    corps = serializers.PrimaryKeyRelatedField(queryset=Corps.objects.all())
    scheme = Base64ImageField(use_url=True)
    photo_gallery = ImageSerializer(many=True, required=False)

    class Meta:
        model = Flat
        exclude = ['gallery']

    def validate(self, attrs):
        if attrs.get('section', None) and attrs.get('floor', None) and attrs.get('corps', None):
            if attrs.get('section', None).house != attrs.get('floor').house != attrs.get('corps').house != self.context.get('house', None):
                raise ValidationError({'corps': _('Корпус, секція та поверх повинні бути с одного будинку'),
                                       'section': _('Корпус, секція та поверх повинні бути с одного будинку'),
                                       'floor': _('Корпус, секція та поверх повинні бути с одного будинку')})
        return super().validate(attrs)

    def update(self, instance: Flat, validated_data):
        gallery = validated_data.pop('image_gallery', None)

        for elem in validated_data.keys():
            setattr(instance, elem, validated_data.get(elem))

        instance.save()

        try:
            if gallery:
                old_image = Image.objects.filter(gallery=instance.gallery)
                for elem in old_image:
                    elem.delete()

                for elem in gallery:
                    photo = Image.objects.create(
                        image=elem.get('image'),
                        gallery=instance.gallery
                    )
                    photo.save()
        except:
            return instance

        return instance

    def to_representation(self, instance: House):
        data = super().to_representation(instance=instance)
        data.update(
            {
                'image_gallery': ImageSerializer(instance=instance.gallery.image_set.all(), many=True).data,
            }
        )
        return data