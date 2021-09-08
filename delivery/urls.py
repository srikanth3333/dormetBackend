from django.urls import path
from . import views

urlpatterns = [
    path('delivery', views.delivery),
    path('order_submission', views.order_submission),
]