from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Image, Gallery


class ImageSerializer(serializers.ModelSerializer):
    """Serializer for Image Model"""
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Image
        exclude = ['id', 'gallery']



class GallerySerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформаціх про галерею
    """
    class Meta:
        model = Gallery
        fields = '__all__'


class ImageListSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про фото з додатковим полем gallery
    """
    gallery = GallerySerializer()

    class Meta:
        model = Image
        fields = '__all__'