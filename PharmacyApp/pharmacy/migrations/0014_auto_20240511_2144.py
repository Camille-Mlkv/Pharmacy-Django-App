# Generated by Django 2.0.1 on 2024-05-11 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0013_auto_20240511_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date_sold',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 11, 21, 44, 32, 225698)),
        ),
    ]
