# Generated by Django 3.2.2 on 2021-09-10 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profiles_images/'),
        ),
    ]