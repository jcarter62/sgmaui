from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='acctview_home'),
#    path('', views.acctview_home, name='acctview_home'),
    path('accounts/', views.accounts, name='accounts'),
    path('account-wells/', views.account_wells, name='account_wells'),
    path('account-wells/<str:account>', views.account_wells, name='account_wells'),
    path('acct-graph-disp', views.acct_graph_disp, name='acct_graph_disp'),
]
