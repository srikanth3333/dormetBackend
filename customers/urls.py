from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login', views.account_login),
    path('otp', views.verify_otp),
]