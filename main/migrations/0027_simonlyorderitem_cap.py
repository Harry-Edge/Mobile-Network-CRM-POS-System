# Generated by Django 3.1.2 on 2020-11-08 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_spendcaps_cap_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='simonlyorderitem',
            name='cap',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.spendcaps'),
        ),
    ]
