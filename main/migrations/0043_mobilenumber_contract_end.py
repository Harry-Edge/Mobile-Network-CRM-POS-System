# Generated by Django 3.1.2 on 2020-11-13 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_simonlyorder_otp_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobilenumber',
            name='contract_end',
            field=models.DateField(null=True),
        ),
    ]