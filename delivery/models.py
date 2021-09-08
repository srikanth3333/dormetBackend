from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Retailer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_agent = models.ForeignKey('DeliveryAgent', on_delete=models.CASCADE)
    assigned_order_complete = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.user.username


class DeliveryAgent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.TextField()
    delivered = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.user.username