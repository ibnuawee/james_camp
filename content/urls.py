from django.urls import path
from .views import AboutContentUpdateView

urlpatterns = [
    path('content/', AboutContentUpdateView.as_view(), name='content_admin'),
]
