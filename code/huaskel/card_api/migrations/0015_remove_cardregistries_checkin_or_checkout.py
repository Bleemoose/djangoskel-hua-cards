# Generated by Django 3.2.8 on 2023-08-07 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card_api', '0014_cardregistries_is_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardregistries',
            name='checkin_or_checkout',
        ),
    ]