# Generated by Django 5.0.6 on 2024-07-24 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottledapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('price', models.CharField(max_length=8)),
                ('image', models.ImageField(null=True, upload_to='image/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='bottledapp.category')),
            ],
        ),
    ]
