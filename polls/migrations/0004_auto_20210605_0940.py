# Generated by Django 2.2.10 on 2021-06-05 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20210605_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='date_start',
            field=models.DateField(blank=True, default=datetime.date.today, editable=False),
        ),
    ]
