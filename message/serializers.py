from rest_framework import serializers
from .models import Chat, Message
from user.models import User
from rest_framework.relations import PrimaryKeyRelatedField


class UserSenderSerializer(serializers.ModelSerializer):
    """
    Цей serializer дозволяє виводити ім'я на прізвище користувача який надіслав повідомлення
    """

    class Meta:
        model = User
        fields = ['name', 'surname']
class ChatContentSerializer(serializers.ModelSerializer):
    """
    Цей serializer дозволяє подивитися id чату та назву
    """

    class Meta:
        model = Chat
        fields = ['id', 'name_chat']

class MessageEasySerializer(serializers.ModelSerializer):
    """
    Цей serializer дозволяє подивитися id повідомлення, його вміст та користувача у якого буде відображатися ім'я та
    прізвище
    """
    user_sender = UserSenderSerializer()
    class Meta:
        model = Message
        fields = ['id', 'content', 'user_sender']

class MessageUpdateSerializer(serializers.ModelSerializer):
    """
    Цей serializer дозволяє виводити тільки вміст повідомлення який надіслав певний користувач
    """

    class Meta:
        model = Message
        fields = ['content']

class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Цей serializer дозволяє подивитися всі повідомлення певного чату
    """
    messages = MessageEasySerializer(many=True)

    class Meta:
        model = Chat
        fields = '__all__'
class MessageSerializer(serializers.ModelSerializer):
    """
    Цей serializer дозволяє отримати повну інформацію про повідомлення а також id та name_chat.
    Та ім'я та прізвище користувача що надіслав повідомлення
    """
    chat = ChatContentSerializer()
    user_sender = UserSenderSerializer()
    class Meta:
        model = Message
        fields = '__all__'

class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Цей serializer дозволяє створити повідомлення де в поле user_sender автоматично буде підставлено авторизованого
    користувача в системі
    """
    chat = PrimaryKeyRelatedField(queryset=Chat.objects.all())
    user_sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Message
        fields = ['content', 'user_sender', 'chat']
        extra_kwargs = {
            'user_sender': {'write_only': True}
        }

