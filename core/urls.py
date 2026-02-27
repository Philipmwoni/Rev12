from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('core/register/', views.register_view, name='register'),
    path('core/', views.home, name='home'),
    path('core/login/', views.login_view, name='login'),
]
