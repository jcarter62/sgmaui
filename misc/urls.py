from django.urls import path
from . import views

urlpatterns = [
    path('account-name/<int:account>', views.account_name, name='account_name'),
    path('account-details/<int:account>', views.account_details, name='account_details'),
    path('well-details/<str:well_id>', views.well_details, name='well_details'),
    path('account-well-count/<int:account>', views.account_well_count, name='account_well_count'),
    path('well-readings/<str:well_id>', views.well_readings, name='well_readings'),
]
