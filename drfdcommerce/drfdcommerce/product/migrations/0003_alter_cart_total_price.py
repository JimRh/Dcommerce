# Generated by Django 4.2.4 on 2023-08-13 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_cart_cartitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(default=0, null=True),
        ),
    ]