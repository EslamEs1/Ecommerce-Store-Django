# Generated by Django 4.0.10 on 2023-03-28 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='products',
            field=models.ManyToManyField(related_name='wishlist', to='products.product'),
        ),
    ]
