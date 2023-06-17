from django.db import models
from user.models import User
# Create your models here.


class Chat(models.Model):
    """
    Модель для чату до якого будуть відноситися повідомлення
    """
    name_chat = models.CharField(max_length=50)
    created_at = models.DateField(auto_created=True, auto_now=True)

class Message(models.Model):
    """
    Модель повідомлень які прив'язанні до чату
    """
    content = models.CharField(max_length=1000)
    sent_at = models.DateField(auto_created=True, auto_now=True)
    user_sender = models.ForeignKey(User, verbose_name='Відправник_повідомлення', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE, related_name='messages')
