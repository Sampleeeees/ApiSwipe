from django.db import models
from house.models import House, Floor, Section, Corps
from user.models import User
from gallery.models import Gallery

class LivingConditionsChoice(models.TextChoices):
    draft = ('draft', 'Чернова')
    repair_required = ('repair', 'Потрібен ремонт')
    good = ('good', 'В жилому стані')


class PlanningChoice(models.TextChoices):
    studio_bathroom = ('studio-bathroom', 'Студія санвузол')
    studio = ('studio', 'Студія')


# Create your models here.
class Flat(models.Model):
    """
    Модель для створення квартири
    """
    room_amount = models.IntegerField()
    scheme = models.ImageField(upload_to='flat/scheme/')
    price = models.FloatField()
    square = models.IntegerField()
    kitchen_square = models.IntegerField()
    balcony = models.BooleanField(default=False)
    commission = models.IntegerField()
    district = models.CharField(max_length=200)
    micro_district = models.CharField(max_length=200)
    living_condition = models.CharField(max_length=50, choices=LivingConditionsChoice.choices, default='draft')
    planning = models.CharField(max_length=50, choices=PlanningChoice.choices, default='studio')
    house = models.ForeignKey(House, verbose_name='Будинок', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, verbose_name='Секція', on_delete=models.CASCADE)
    corps = models.ForeignKey(Corps, verbose_name='Корпус', on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, verbose_name='Поверх', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Будівельник', on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея', on_delete=models.CASCADE)
