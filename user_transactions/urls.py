from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.member_transaction_categories, name='member_transaction_categories'),
    path('transactions/category/<int:category_id>/', views.member_transaction_items, name='member_transaction_items'),
    path('transactions/item/<int:item_id>/', views.member_transaction_form, name='member_transaction_form'),
    path('transactions/detail/<int:transaction_id>/', views.member_transaction_detail, name='member_transaction_detail'),
    path('transactions/list/', views.member_transaction_list, name='member_transaction_list'),
]
