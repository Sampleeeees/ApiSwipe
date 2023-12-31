from rest_framework import serializers
from .models import Favorite
from message.serializers import UserSenderSerializer
from announcement.serializers import AnnouncementBaseSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer для виводу даних улюблених оголошень з додатковим описом про user, announcement
    """
    user = UserSenderSerializer()
    announcement = AnnouncementBaseSerializer()

    class Meta:
        model = Favorite
        fields = '__all__'

class FavoriteUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer для оновлення інформації про улюблені оголошення
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only'}
        }