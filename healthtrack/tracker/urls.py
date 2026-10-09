from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_measurement, name='add_measurement'),
    path('edit/<int:pk>/', views.edit_measurement, name='edit_measurement'),
    path('delete/<int:pk>/', views.delete_measurement, name='delete_measurement'),
    path('export/', views.export_csv, name='export_csv'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]