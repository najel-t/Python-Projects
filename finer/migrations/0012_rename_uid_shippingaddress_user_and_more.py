# Generated by Django 5.0 on 2023-12-16 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finer', '0011_shippingaddress_pid_shippingaddress_uid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='uid',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='pid',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='products',
            field=models.ManyToManyField(to='finer.product'),
        ),
    ]