# Generated by Django 3.2.2 on 2021-08-30 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20210828_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='retailer_assigned',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
