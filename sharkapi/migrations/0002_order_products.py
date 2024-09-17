# Generated by Django 5.1.1 on 2024-09-17 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharkapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='sharkapi.OrderItem', to='sharkapi.product'),
        ),
    ]
