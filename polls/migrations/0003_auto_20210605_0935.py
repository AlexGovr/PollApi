# Generated by Django 2.2.10 on 2021-06-05 06:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_questionchoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='date_end',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='date_start',
            field=models.DateField(blank=True, default=datetime.datetime.today, editable=False),
        ),
    ]
