# Generated by Django 3.2.8 on 2023-08-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_api', '0013_alter_cardregistries_checkin_or_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardregistries',
            name='is_checkout',
            field=models.BooleanField(default=False),
        ),
    ]
