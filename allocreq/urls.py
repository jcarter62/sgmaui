from django.urls import path
from . import views

urlpatterns = [
    path('', views.ar_home, name='ar_home'),
]