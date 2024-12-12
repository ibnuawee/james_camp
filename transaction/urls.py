from django.urls import path
from . import views

urlpatterns = [
    # Daftar Transaksi
    path('', views.transaction_list, name='transaction_list'),

    # Tambah Transaksi
    path('transactions/add/', views.transaction_create, name='transaction_create'),

    # Edit Transaksi
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
]
