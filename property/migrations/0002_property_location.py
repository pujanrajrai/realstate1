# Generated by Django 4.0.3 on 2022-03-07 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='location',
            field=models.CharField(default='no location', max_length=100),
        ),
    ]
