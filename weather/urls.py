from django.urls import path

from . import views

urlpatterns = [
    path('tri-hourly/', views.tri_hourly, name='tri-hourly'),
    path('current/', views.current, name='current'),
    path('', views.index, name='index'),
]