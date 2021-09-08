from django.db import models
from django.contrib.auth.models import User

# Create your models here.
USER_ROLES  =(
    ("1", "Customer"),
    ("2", "Admin"),
    ("3", "Retailer"),
)
  


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.PositiveIntegerField()
    otp = models.PositiveIntegerField()
    role = models.CharField(choices = USER_ROLES, max_length=20,blank=True)

    def __str__(self):
        return self.user.username