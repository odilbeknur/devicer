# Generated by Django 5.0.2 on 2024-03-27 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_inventar_number_device_inventory_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='serial_number',
        ),
    ]
