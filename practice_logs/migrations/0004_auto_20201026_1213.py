# Generated by Django 3.1.2 on 2020-10-26 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('practice_logs', '0003_auto_20201026_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='person_of',
        ),
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(null=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=-1,
        ),
    ]