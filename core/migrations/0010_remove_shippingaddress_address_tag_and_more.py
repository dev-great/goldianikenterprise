# Generated by Django 5.0 on 2024-01-14 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_contactus_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='address_tag',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='alternate_phone_number',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='delivery_address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
    ]
