from django.db import models
from user.models import User
from gallery.models import Gallery
# Create your models here.

class HouseStatusChoices(models.TextChoices):
    """
    Choices для вибору стану будинку
    """
    flats = 'flats', 'Квартири'
    cottage = 'cottage', 'Котедж'
    new_buildings = 'new-buildings', 'Новобудови'
    secondary_market = 'secondary-market', 'Вторинний ринок'

class HouseTypeChoices(models.TextChoices):
    """
    Choices для вибору типу будинку
    """
    many_floors = 'many-floors', 'Багатоквартирна'
    office = 'office', 'Офіс'
    hostel = 'hostel', 'Готель'

class HouseClassChoices(models.TextChoices):
    """
    Choices для вибору класу будинку
    """
    lux = 'lux', 'Люкс'
    elite = 'elite', 'Елітний'
    common = 'common', 'Стандартний'
    poor = 'poor', 'Дешевий'


class BuildingTechnologyChoices(models.TextChoices):
    """
    Choices для вибору технології будування
    """
    frame = 'frame', 'Монолітний каркас'
    brick = 'brick', 'Цегла'
    foam = 'foam', 'Піноблок'


class TerritoryChoices(models.TextChoices):
    """
    Choices для вибору типу території
    """
    close = 'close', 'Закрита'
    open = 'open', 'Відкрита'
    protected = 'protected', 'Під охороною'


class CeilingChoices(models.TextChoices):
    """
    Choices для вибору висоти стелі у метрах
    """
    two = 2
    three = 3


class HeatingChoices(models.TextChoices):
    """
    Choices для вибору типу опалення
    """
    central = 'central', 'Центральне'
    autonomous = 'autonomous', 'Автономне'

class SewerageChoices(models.TextChoices):
    """
    Choices для вибору типу каналізації
    """
    central = 'central', 'Центральне'
    autonomous = 'autonomous', 'Автономне'


class WaterSupplyChoices(models.TextChoices):
    """
    Choices для вибору типу води
    """
    central = 'central', 'Центральне'
    autonomous = 'autonomous', 'Автономне'

class ArrangementChoices(models.TextChoices):
    """
    Choices для вибору типу укладення угоди
    """
    justice = 'justice', 'Юстиція'
    finance = 'finance', 'Фінанси'


class PaymentChoices(models.TextChoices):
    """
    Choices для вибору типу оплати
    """
    mortgage = 'mortgage', 'Іпотека'
    parent_capital = 'parent-capital', 'Материнський капітал'


class ContractSumChoices(models.TextChoices):
    """
    Choices для вибору типу контракту
    """
    full = 'full', 'Повна'
    part = 'part', 'Частинами'


class PropertyChoices(models.TextChoices):
    """
    Choices для вибору типу стану приміщення
    """
    living_building = 'living_building', 'Живе приміщення'


class House(models.Model):
    """Model House"""
    name = models.CharField(max_length=50)
    general_image = models.ImageField(upload_to='house/general_photo/')
    address = models.CharField(max_length=100)
    map_position = models.CharField(max_length=350)
    min_price = models.FloatField()
    price_for_m2 = models.IntegerField()
    area = models.FloatField()
    description = models.CharField(max_length=850)
    status_house = models.CharField(max_length=50, choices=HouseStatusChoices.choices, default='flats')
    type_house = models.CharField(max_length=50, choices=HouseTypeChoices.choices, default='many-floors')
    class_house = models.CharField(max_length=50, choices=HouseClassChoices.choices, default='common')
    building_technology = models.CharField(max_length=50, choices=BuildingTechnologyChoices.choices, default='frame')
    territory = models.CharField(max_length=50, choices=TerritoryChoices.choices, default='close')
    sea_distance = models.IntegerField()
    celling_height = models.CharField(max_length=50, choices=CeilingChoices.choices, default=2)
    gas = models.BooleanField(default=True)
    heating = models.CharField(max_length=50, choices=HeatingChoices.choices, default='central')
    electricity = models.BooleanField(default=True)
    sewerage = models.CharField(max_length=50, choices=SewerageChoices.choices, default='central')
    water_supply = models.CharField(max_length=50, choices=WaterSupplyChoices.choices, default='central')
    arrangement = models.CharField(max_length=50, choices=ArrangementChoices.choices, default='justice')
    payment = models.CharField(max_length=50, choices=PaymentChoices.choices, default='mortgage')
    contract_sum = models.CharField(max_length=50, choices=ContractSumChoices.choices, default='full')
    property_status = models.CharField(max_length=50, choices=PropertyChoices.choices, default='living_building')
    builder = models.ForeignKey(User, verbose_name='Забудовник', on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея', on_delete=models.CASCADE)


class Section(models.Model):
    """Model Section for House"""
    name = models.CharField(max_length=70)
    house = models.ForeignKey(House, verbose_name='Будинок', on_delete=models.CASCADE)

class Floor(models.Model):
    """Model Floor for House"""
    name = models.CharField(max_length=70)
    house = models.ForeignKey(House, verbose_name='Будинок', on_delete=models.CASCADE)

class Corps(models.Model):
    """Model Corps for House"""
    name = models.CharField(max_length=70)
    house = models.ForeignKey(House, verbose_name='Будинок', on_delete=models.CASCADE)


class Document(models.Model):
    """Model Document for House"""
    name = models.CharField(max_length=70)
    file = models.FileField(upload_to='house/document/')
    house = models.ForeignKey(House, verbose_name='Будинок', on_delete=models.CASCADE)

class News(models.Model):
    """Model News for House"""
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=450)
    date = models.DateField(auto_now_add=True)
    house = models.ForeignKey(House, verbose_name='Будинок', on_delete=models.CASCADE)


