# Generated by Django 3.1.2 on 2020-11-18 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_mobilenumber_annual_upgrade'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobilenumber',
            name='mrc',
            field=models.FloatField(null=True),
        ),
    ]
