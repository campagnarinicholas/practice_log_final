# Generated by Django 3.1.2 on 2020-11-10 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0009_auto_20201110_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='skill_entry',
        ),
        migrations.AddField(
            model_name='skill_entry',
            name='skill',
            field=models.ManyToManyField(to='practice_logs.Skill'),
        ),
    ]