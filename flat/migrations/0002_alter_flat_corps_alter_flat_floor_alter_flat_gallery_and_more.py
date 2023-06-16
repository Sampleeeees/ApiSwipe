# Generated by Django 4.2.2 on 2023-06-15 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
        ('house', '0002_rename_general_photo_house_general_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='corps',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.corps', verbose_name='Корпус'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='floor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.floor', verbose_name='Поверх'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='gallery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.gallery', verbose_name='Галерея'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.house', verbose_name='Будинок'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='house.section', verbose_name='Секція'),
        ),
        migrations.AlterField(
            model_name='flat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Будівельник'),
        ),
    ]
