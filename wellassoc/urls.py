from django.urls import path
from . import views

urlpatterns = [
    path('', views.wa_home, name='wa_home'),
]