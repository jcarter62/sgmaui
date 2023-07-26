from django.urls import path
from . import views

urlpatterns = [
    path('', views.readings_home, name='readings_home'),
    path('manual/', views.readings_manual, name='readings_manual'),
    path('ui/', views.readings_ui, name='readings_ui'),
]
