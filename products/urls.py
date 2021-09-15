from django.urls import path
from . import views

urlpatterns = [
    path('addProduct', views.add_product),
    path('profile', views.profile),
    path('favourites', views.favourites),
    path('track_order/<int:pk>', views.track_order),
    path('order_summary/<int:pk>', views.order_summary),
    path('cart_list', views.cart_list),
    path('my_orders', views.my_orders),
    path('payment', views.payment),
    path('review', views.review),
    path('shopProducts/<int:pk>', views.shopProducts),
    path('listOfProducts', views.get_products),
    path('allRatings', views.all_ratings),
    path('listOfProducts/<int:pk>', views.product_detail),
    path('productRatings/<int:pk>', views.productRatings),
    path('add_product_ratings/', views.add_product_ratings),
    path('cart_count/', views.cart_count),
    path('listOfShops', views.get_shops),
    path('add_to_cart', views.add_to_cart),
    path('remove_from_cart', views.remove_from_cart),
    path('remove_single_item_from_cart', views.remove_single_item_from_cart),
    path('add_comments', views.add_comments),
    path('billing', views.billing_address),
    path('shop_create', views.shops_create),
    path('order_confirm', views.order_confimrations),
]