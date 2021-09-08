from django.contrib import admin
from .models import Products, OrderedItem, Order, Comments, BillingAddress, Shops

# Register your models here.
admin.site.register(Products)
admin.site.register(OrderedItem)
admin.site.register(Order)
admin.site.register(Comments)
admin.site.register(BillingAddress)
admin.site.register(Shops)
admin.site.site_header = 'Dormet  Ecommerce'