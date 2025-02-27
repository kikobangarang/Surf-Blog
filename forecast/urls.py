from django.urls import path
from . import views

app_name = 'forecast'

urlpatterns = [
    path('', views.surf_breaks, name='surf_breaks'),
    path('<str:break_name>/', views.index, name='index'),
]