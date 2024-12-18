"""define URL model for app users"""
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # 包含默认的身份验证URL
    path('', include('django.contrib.auth.urls')),
    # login page
    path('register/', views.register, name='register'),
]
