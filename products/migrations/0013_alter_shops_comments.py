# Generated by Django 3.2.2 on 2021-09-09 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_shops_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shops',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
