# Generated by Django 4.0.3 on 2022-03-10 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
