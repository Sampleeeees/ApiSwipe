from rest_framework import serializers
from .models import ChessBoard
from house.serializers import CorpsApiSerializer, SectionApiSerializer, FloorApiSerializer, HouseListSerializer
from house.models import *
from .models import Flat



class FlatListSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про квартиру з полями схеми та ціни
    """
    class Meta:
        model = Flat
        fields = ['scheme', 'price']

class ChessboardSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про шахматку з додатковим описом полів house, section, floor, corps, flat
    """
    house = HouseListSerializer()
    section = SectionApiSerializer()
    floor = FloorApiSerializer()
    corps = CorpsApiSerializer()
    flat = FlatListSerializer()

    class Meta:
        model = ChessBoard
        fields = '__all__'

class ChessboardUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer для оновлення шахматки
    """
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    corps = serializers.PrimaryKeyRelatedField(queryset=Corps.objects.all())

    class Meta:
        model = ChessBoard
        fields = ['section', 'corps']