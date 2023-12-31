# Generated by Django 4.2.2 on 2023-06-15 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_created=True, auto_now=True)),
                ('name_chat', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateField(auto_created=True, auto_now=True)),
                ('content', models.CharField(max_length=1000)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.chat', verbose_name='Чат')),
                ('user_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Відправник_повідомлення')),
            ],
        ),
    ]
