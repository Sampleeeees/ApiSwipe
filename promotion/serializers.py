from rest_framework import serializers
from .models import *



class PromotionSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних моделі Promotion
    """
    class Meta:
        model = Promotion
        fields = '__all__'