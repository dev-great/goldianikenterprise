# Generated by Django 5.0 on 2024-01-15 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_shippingaddress_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
