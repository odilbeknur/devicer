# Generated by Django 5.0.2 on 2024-04-02 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_device_inventory_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='device',
            name='memory',
        ),
        migrations.RemoveField(
            model_name='device',
            name='processor',
        ),
    ]
