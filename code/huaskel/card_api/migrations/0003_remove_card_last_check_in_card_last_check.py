# Generated by Django 4.1.7 on 2023-03-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_api', '0002_rename_owner_id_card_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='last_check_in',
        ),
        migrations.AddField(
            model_name='card',
            name='last_check',
            field=models.DateField(auto_now=True),
        ),
    ]