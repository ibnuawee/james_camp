from django.urls import path
from . import views
from .views import BlogDetailView

urlpatterns = [
    path('', views.member_dashboard, name='home'),
    path('price/', views.price, name='price'),
    path('about/', views.about_page, name='about'),
    path('blog/', views.list_blog, name='list_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='detail_blog'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

