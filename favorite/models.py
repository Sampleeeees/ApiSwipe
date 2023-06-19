from django.db import models
from announcement.models import Announcement
from user.models import User

# Create your models here.
class Favorite(models.Model):
    """
    Модель для збереження обраних заявок для користувача
    """
    announcement = models.ForeignKey(Announcement, verbose_name='Заявка', on_delete=models.CASCADE, limit_choices_to={'confirm': True})
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)