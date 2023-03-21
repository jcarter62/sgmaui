from django.urls import path
from . import views

urlpatterns = [
    path('', views.acctview_home, name='acctview_home'),
    path('accounts/', views.acccounts, name='acccounts'),
    path('account-wells/', views.account_wells, name='account_wells'),
    path('account-wells/<str:account>', views.account_wells, name='account_wells'),

]
