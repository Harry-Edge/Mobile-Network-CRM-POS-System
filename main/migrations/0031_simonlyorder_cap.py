# Generated by Django 3.1.2 on 2020-11-09 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20201109_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='simonlyorder',
            name='cap',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.spendcaps'),
        ),
    ]
