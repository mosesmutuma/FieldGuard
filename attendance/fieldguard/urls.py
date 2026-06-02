from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_login, name='staff_login'),
    path('dashboard/', views.field_dashboard, name='field_dashboard'),
    path('process-checkin/', views.process_checkin, name='process_checkin'),
    path('logout/', views.staff_logout, name='staff_logout'),
]