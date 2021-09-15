# Generated by Django 3.2.2 on 2021-09-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20210913_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='quantity_in_grams',
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='quantity_in_grams',
            field=models.CharField(blank=True, choices=[('50grams', '50GRAMS'), ('100grams', '100GRAMS'), ('1kg', '1KG'), ('2kg', '2KG'), ('3kg', '3KG')], default='50GRAMS', max_length=150, null=True),
        ),
    ]
