# Generated by Django 3.1.2 on 2020-11-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0010_auto_20201110_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill_entry',
            name='description',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
