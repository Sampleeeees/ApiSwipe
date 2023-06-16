from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Image


class ImageSerializer(serializers.Serializer):
    """Serializer for Image Model"""
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Image
        exclude = ['id', 'gallery']