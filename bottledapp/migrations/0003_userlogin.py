# Generated by Django 5.0.6 on 2024-08-06 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottledapp', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userlogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('mobile_number', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('otp_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
