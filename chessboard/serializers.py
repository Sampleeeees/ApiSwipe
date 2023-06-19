from rest_framework import serializers
from .models import ChessBoard
from house.serializers import CorpsApiSerializer, SectionApiSerializer, FloorApiSerializer, HouseListSerializer
from house.models import *
from .models import Flat



class FlatListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flat
        fields = ['scheme', 'price']

class ChessboardSerializer(serializers.ModelSerializer):
    house = HouseListSerializer()
    section = SectionApiSerializer()
    floor = FloorApiSerializer()
    corps = CorpsApiSerializer()
    flat = FlatListSerializer()

    class Meta:
        model = ChessBoard
        fields = '__all__'

class ChessboardUpdateSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    corps = serializers.PrimaryKeyRelatedField(queryset=Corps.objects.all())

    class Meta:
        model = ChessBoard
        fields = ['section', 'corps']