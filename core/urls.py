from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    path('login/', views.login_view, name='login'),

]
