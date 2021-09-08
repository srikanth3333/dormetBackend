from django.contrib import admin
from .models import DeliveryAgent, Retailer

# Register your models here.
admin.site.register(DeliveryAgent)
admin.site.register(Retailer)