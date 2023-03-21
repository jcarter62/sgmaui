from django.urls import path
from . import views

urlpatterns = [
    path('', views.au_home, name='au_home'),
]