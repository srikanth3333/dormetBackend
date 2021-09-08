# Generated by Django 3.2.2 on 2021-08-30 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryagent',
            name='delivered',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_order_complete', models.BooleanField(blank=True, default=False)),
                ('assigned_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.deliveryagent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]