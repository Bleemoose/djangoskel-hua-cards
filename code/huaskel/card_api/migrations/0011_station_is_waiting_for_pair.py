# Generated by Django 3.2.8 on 2023-07-18 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_api', '0010_card_physical_card_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='is_waiting_for_pair',
            field=models.BooleanField(default=False),
        ),
    ]
