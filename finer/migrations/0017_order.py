# Generated by Django 5.0 on 2024-01-05 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finer', '0016_shippingaddress_payment_mode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('pincode', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('payment_mode', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
