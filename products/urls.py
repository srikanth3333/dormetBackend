from django.urls import path
from . import views

urlpatterns = [
    path('addProduct', views.add_product),
    path('listOfProducts', views.get_products),
    path('add_to_cart', views.add_to_cart),
    path('remove_from_cart', views.remove_from_cart),
    path('remove_single_item_from_cart', views.remove_single_item_from_cart),
    path('add_comments', views.add_comments),
    path('billing', views.billing_address),
    path('shop_create', views.shops_create),
    path('order_confirm', views.order_confimrations),
]