from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/chart-data/', views.chart_data_api, name='chart_data'),
]









