from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    category_name = models.CharField(max_length=200)


    def __str__(self):
        return self.category_name