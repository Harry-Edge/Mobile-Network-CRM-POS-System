# Generated by Django 3.1.2 on 2020-10-30 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_addons_simonlyorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simonlyorder',
            old_name='customer',
            new_name='cus',
        ),
    ]
