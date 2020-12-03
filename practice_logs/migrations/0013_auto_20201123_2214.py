# Generated by Django 3.1.2 on 2020-11-24 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0012_auto_20201116_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill_entry',
            name='skill',
        ),
        migrations.AddField(
            model_name='skill_entry',
            name='skill',
            field=models.ForeignKey(null=-1, on_delete=django.db.models.deletion.CASCADE, to='practice_logs.skill'),
            preserve_default=-1,
        ),
    ]
