from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_dashboard, name='home'),
    path('price/', views.price, name='price'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
]

