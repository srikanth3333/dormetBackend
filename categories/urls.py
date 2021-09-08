from django.urls import path
from . import views

urlpatterns = [
    path('addCategory', views.add_category),
    path('listOfCategories', views.get_categories),
]