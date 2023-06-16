from django.db import models
from house.models import House, Section, Floor, Corps
from flat.models import Flat
# Create your models here.

class ChessBoard(models.Model):
    """
    Модель для шахматки квартири
    """
    house = models.ForeignKey(House, verbose_name='Будинок', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, verbose_name='Секція', on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, verbose_name='Поверх', on_delete=models.CASCADE)
    corps = models.ForeignKey(Corps, verbose_name='Корпус', on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, verbose_name='Квартира', on_delete=models.CASCADE)
