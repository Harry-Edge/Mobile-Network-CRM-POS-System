# Generated by Django 3.1.2 on 2020-11-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_auto_20201121_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='handsets',
            name='colour',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
