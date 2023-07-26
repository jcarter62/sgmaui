from django.urls import path
from . import views

urlpatterns = [
    path('', views.mp_home, name='mp_home'),
    path('parcels/', views.mp_parcels, name='mp_parcels'),
    path('parcels/parcel-details/<str:parcel_id>/', views.mp_parcel_details, name='mp_parcel_details'),
]

