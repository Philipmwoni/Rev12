from django.urls import path
from . import views

app_name = 'Auth'

urlpatterns = [
    path('', views.home, name='home'),
    path('chart-data/', views.chart_data_api, name='chart_data_api'),
]
from django.urls import path
from . import views

app_name = 'Auth'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/chart-data/', views.chart_data_api, name='chart_data'),
]









