# Generated by Django 3.1.2 on 2020-11-28 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0060_simonlyorder_friends_and_family'),
    ]

    operations = [
        migrations.AddField(
            model_name='simonlyorder',
            name='handset_credit',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
