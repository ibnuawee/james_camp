from django.urls import path
from . import views

urlpatterns = [
    # Daftar Transaksi
    path('', views.transaction_list, name='transaction_list'),

    # Tambah Transaksi
    path('transactions/add/', views.transaction_create, name='transaction_create'),

    # Edit Transaksi
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),

    path('payment-methods/', views.payment_method_list, name='payment_method_list'),
    path('payment-methods/add/', views.payment_method_create, name='payment_method_create'),
    path('payment-methods/<int:pk>/edit/', views.payment_method_update, name='payment_method_update'),
    path('payment-methods/<int:pk>/delete/', views.payment_method_delete, name='payment_method_delete'),
]
