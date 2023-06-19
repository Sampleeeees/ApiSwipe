from rest_framework import serializers
from .models import Filter
from message.serializers import UserSenderSerializer

class FilterSerializer(serializers.ModelSerializer):
    """
    Serializer для опису даних пр бережені фільтри
    """
    user = UserSenderSerializer()

    class Meta:
        model = Filter
        fields = '__all__'

class FilterSaveSerializer(serializers.ModelSerializer):
    """
    Serializer для збереження фільтрів та автоматично зберегти авторизованого користувача як creator
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Filter
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }
