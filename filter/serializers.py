from rest_framework import serializers
from .models import Filter
from message.serializers import UserSenderSerializer

class FilterSerializer(serializers.ModelSerializer):
    user = UserSenderSerializer()

    class Meta:
        model = Filter
        fields = '__all__'

class FilterSaveSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Filter
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True}
        }
