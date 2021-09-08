# Generated by Django 3.2.2 on 2021-08-28 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20210828_1018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=200)),
                ('ratings', models.CharField(max_length=5)),
                ('comments', models.TextField(max_length=5)),
                ('products', models.ManyToManyField(blank=True, to='products.Products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
