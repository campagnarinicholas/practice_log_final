# Generated by Django 3.1.2 on 2020-11-16 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('practice_logs', '0011_skill_entry_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill_entry',
            name='user',
            field=models.ForeignKey(null=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
