# Generated by Django 3.2.7 on 2021-09-23 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_cart_order_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='order_checkout',
            field=models.BooleanField(default=False, null=True),
        ),
    ]