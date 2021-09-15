from django.urls import path
from . import views

urlpatterns = [
    path('addCategory', views.add_category),
    path('listOfCategories', views.get_categories),
    path('search_products/', views.search_products),
    path('categoryProducts/<int:pk>', views.get_category_products),
]