from django.db import models
from user.models import User
from house.models import HouseStatusChoices, HouseTypeChoices, PaymentChoices, PropertyChoices
# Create your models here.

class LivingConditionsChoice(models.TextChoices):
    draft = ('draft', 'Чернова')
    repair_required = ('repair', 'Потрібен ремонт')
    good = ('good', 'В жилому стані')

class Filter(models.Model):
    """
    Модель для збережених фільтрів користувача
    """
    type_property = models.CharField(max_length=50, choices=PropertyChoices.choices, default='living_building')
    status_home = models.CharField(max_length=50, choices=HouseStatusChoices.choices, default='flats')
    district = models.CharField(max_length=50)
    micro_district = models.CharField(max_length=50)
    room_count = models.CharField(max_length=50)
    min_price = models.IntegerField(default=1)
    max_price = models.IntegerField(default=99999)
    min_area = models.IntegerField(default=1)
    max_area = models.IntegerField(default=99999)
    purpose = models.CharField(max_length=50, choices=HouseTypeChoices.choices, default='many_floors')
    purchase_terms = models.CharField(max_length=50, choices=PaymentChoices.choices, default='mortgage')
    condition = models.CharField(max_length=50, choices=LivingConditionsChoice.choices, default='draft')
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)

