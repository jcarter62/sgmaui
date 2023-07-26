from django.urls import path
from . import views

urlpatterns = [
#    path('', views.mw_home, name='mw_home'),
    path('', views.display_wells, name='mw_home'),
    path('wells/', views.display_wells, name='display_wells'),
    path('display-well-details/<str:well_id>', views.display_well_details, name='display_well_details'),
    path('save-well-details/', views.save_well_details, name='save_well_details'),
    path('reorder-well-records/<str:well_id>', views.reorder_well_records, name='reorder_well_records'),
    path('add-well-assoc-record/<str:well_id>', views.add_well_assoc_record, name='add_well_assoc_record'),
]
