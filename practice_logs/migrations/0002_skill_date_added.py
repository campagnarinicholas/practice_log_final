# Generated by Django 3.1.2 on 2020-10-06 20:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
