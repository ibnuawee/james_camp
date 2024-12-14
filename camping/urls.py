from django.urls import path
from . import views

urlpatterns = [

    path('', views.camping_item_list, name='camping_item_list'),
    path('item/add/', views.camping_item_create, name='camping_item_create'),
    path('item/<int:pk>/edit/', views.camping_item_update, name='camping_item_update'),
    path('item/<int:pk>/delete/', views.camping_item_delete, name='camping_item_delete'),

    path('category', views.camping_category, name='category_list'),
    path('category/add/', views.category_create, name='category_create'),
    path('category/<int:pk>/edit/', views.category_item_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
