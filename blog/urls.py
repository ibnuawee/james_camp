from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView,
    BlogUpdateView, BlogDeleteView, BlogCategoryListView,
    BlogCategoryCreateView,
    BlogCategoryUpdateView,
    BlogCategoryDeleteView
)

urlpatterns = [
    path('list', BlogListView.as_view(), name='blog_list'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),

    path('categories/', BlogCategoryListView.as_view(), name='blog_category_list'),
    path('categories/create/', BlogCategoryCreateView.as_view(), name='blog_category_create'),
    path('categories/<int:pk>/update/', BlogCategoryUpdateView.as_view(), name='blog_category_update'),
    path('categories/<int:pk>/delete/', BlogCategoryDeleteView.as_view(), name='blog_category_delete'),
]
