# Generated by Django 3.2.2 on 2021-08-28 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_products_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shops',
            name='comments',
            field=models.TextField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='shops',
            name='ratings',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]
