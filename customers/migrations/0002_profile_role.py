# Generated by Django 3.2.2 on 2021-08-28 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[('1', 'Customer'), ('2', 'Admin'), ('3', 'Retailer')], max_length=20),
        ),
    ]
