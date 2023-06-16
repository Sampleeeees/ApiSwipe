from django.db import models

# Create your models here.
class Gallery(models.Model):
    """
    Модель для галереї
    """
    text = models.CharField(max_length=50, default='New Gallery')

class Image(models.Model):
    """
    Модель для фото які прив'язані до галереї
    """
    image = models.ImageField(upload_to='gallery/image/')
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея', on_delete=models.CASCADE)