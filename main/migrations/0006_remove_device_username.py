# Generated by Django 5.0.2 on 2024-04-02 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_device_ip_address_remove_device_memory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='username',
        ),
    ]
