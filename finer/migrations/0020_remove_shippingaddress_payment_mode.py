# Generated by Django 5.0 on 2024-01-09 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finer', '0019_remove_shippingaddress_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='payment_mode',
        ),
    ]