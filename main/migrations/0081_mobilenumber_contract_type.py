# Generated by Django 3.1.2 on 2021-02-25 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_auto_20210121_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobilenumber',
            name='contract_type',
            field=models.CharField(choices=[('Handset', 'Handset'), ('Simo', 'Simo')], max_length=10, null=True),
        ),
    ]