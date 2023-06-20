from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from message.models import Chat, Message
from user.models import User

class Command(BaseCommand):
    help = _('Створення чатів та повідомлень')

    def handle(self, *args, **options):

        # Create chats
        chat1 = Chat.objects.create(name_chat='First chat')
        chat2 = Chat.objects.create(name_chat='Second chat')
        print('Create chats')

        admin = User.objects.filter(role__is_admin=True).first()
        builder = User.objects.filter(role__is_builder=True).first()
        manager = User.objects.filter(role__is_manager=True).first()

        message1 = Message.objects.create(
            content='Hello Builder',
            user_sender=admin,
            chat=chat1
        )

        message2 = Message.objects.create(
            content='Hello admin',
            user_sender=builder,
            chat=chat1
        )

        message3 = Message.objects.create(
            content='Hello Manager',
            user_sender=admin,
            chat=chat2
        )

        message4 = Message.objects.create(
            content='Hello admin',
            user_sender=manager,
            chat=chat2
        )

        print('Message created')
