# Generated by Django 5.0.6 on 2024-08-24 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottledapp', '0005_alter_cart_product_alter_cart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogin',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userlogin',
            name='mobile_number',
            field=models.CharField(max_length=15),
        ),
    ]
