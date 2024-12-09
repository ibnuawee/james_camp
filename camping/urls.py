from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('member_dashboard/', views.member_dashboard, name='member_dashboard'),
    path('', views.camping_item_list, name='camping_item_list'),
    path('item/add/', views.camping_item_create, name='camping_item_create'),
    path('item/<int:pk>/edit/', views.camping_item_update, name='camping_item_update'),
    path('item/<int:pk>/delete/', views.camping_item_delete, name='camping_item_delete'),
    path('category/add/', views.category_create, name='category_create'),
]
