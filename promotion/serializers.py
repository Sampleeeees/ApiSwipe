from rest_framework import serializers
from .models import *



class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = '__all__'