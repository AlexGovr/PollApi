# Generated by Django 2.2.10 on 2021-06-05 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_delete_questionchoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='questions',
        ),
        migrations.AddField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
            preserve_default=False,
        ),
    ]
