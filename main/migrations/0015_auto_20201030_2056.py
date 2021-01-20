# Generated by Django 3.1.2 on 2020-10-30 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20201030_2041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simonlyorder',
            old_name='date_order',
            new_name='date_ordered',
        ),
        migrations.CreateModel(
            name='SimOnlyOrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('date_ordered', models.DateTimeField(null=True)),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.simonlytariffs')),
            ],
        ),
    ]
