from django.urls import path
from . import views

urlpatterns = [
    path('input-params', views.gw_input_params, name='gw_input_params'),
    path('gw_view_calc_results', views.gw_view_calc_results, name='gw_view_calc_results'),
    path('gw_export_calc_results', views.gw_export_calc_results, name='gw_export_calc_results'),
    path('gw_export_calc_results_xlsx', views.gw_export_calc_results_xlsx, name='gw_export_calc_results_xlsx'),
]
