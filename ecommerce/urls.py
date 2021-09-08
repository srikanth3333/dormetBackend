
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('customers.urls')),
    path('category/',include('categories.urls')),
    path('products/',include('products.urls')),
    path('delivery/',include('delivery.urls')),
]
