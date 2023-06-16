from django.db import models
from flat.models import Flat
# Create your models here.
class Announcement(models.Model):
    """
    Модель для заявки
    """
    confirm = models.BooleanField()
    flat = models.ForeignKey(Flat, verbose_name='Кватира', on_delete=models.CASCADE)
