# Generated by Django 4.0.10 on 2023-03-28 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_wishlist_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='products',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]
