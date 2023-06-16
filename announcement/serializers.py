from rest_framework import serializers
from announcement.models import Announcement
from flat.models import Flat
from house.models import Floor, Section, Corps
from user.models import User

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']


class FloorInfoSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про поверхи для flat в Announcement
    """
    class Meta:
        model = Floor
        fields = ['id', 'name']


class SectionInfoSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про секції для flat в Announcement
    """
    class Meta:
        model = Section
        fields = ['id', 'name']


class CorpsInfoSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу інформації про корпуси для flat в Announcement
    """
    class Meta:
        model = Corps
        fields = ['id', 'name']


class FlatFullSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу повної інформації про те де знаходиться квартира
    """
    floor = FloorInfoSerializer()
    section = SectionInfoSerializer()
    corps = CorpsInfoSerializer()
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Flat
        fields = ['id', 'scheme', 'price', 'square', 'floor', 'section', 'corps', 'user']


class AnnouncementBaseSerializer(serializers.ModelSerializer):
    """
    Serializer для можливості змінити flat в методі patch
    """
    flat = serializers.PrimaryKeyRelatedField(queryset=Flat.objects.all(), allow_null=True)

    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    Serializer для отримання інформації про оголошення
    """
    flat = FlatFullSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementIdSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу всіх існуючих моделей announcement
    """
    class Meta:
        model = Announcement
        fields = ['id']
