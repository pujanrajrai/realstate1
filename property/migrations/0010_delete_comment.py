# Generated by Django 4.0.3 on 2022-03-08 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_comment_date_of_added'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]