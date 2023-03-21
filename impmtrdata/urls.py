from django.urls import path
from . import views

urlpatterns = [
    path('', views.imd_home, name='imd_home'),
]