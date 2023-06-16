from django.db import models
from announcement.models import Announcement
# Create your models here.
class Promotion(models.Model):
    """
    Модель для продвигу оголошення
    """
    highlight = models.BooleanField(default=False)
    phrase = models.BooleanField(default=False)
    big_announcement = models.BooleanField(default=False)
    turbo = models.BooleanField(default=False)
    raised = models.BooleanField(default=False)
    date = models.DateField(auto_created=True, auto_now=True)
    price = models.IntegerField(default=250)
    announcement = models.ForeignKey(Announcement, verbose_name='Заявка', on_delete=models.CASCADE)