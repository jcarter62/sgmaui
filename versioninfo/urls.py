from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name='version_info_home'),
    ]