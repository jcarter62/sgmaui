from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name='home'),
    # path('about/', view_about, name='about'),
    # path('contact/', view_contact, name='contact'),
    path('faq', views.view_faq, name='faq'),
    # path('privacy/', view_privacy, name='privacy'),
    # path('terms/', view_terms, name='terms'),
    # path('login/', view_login, name='login'),
    path('user-settings', views.view_user_settings, name='user-settings'),
    path('showenv/', views.view_showenv, name='showenv'),
    path('params/set/<str:session>/<str:key>/<str:value>', views.view_set_param, name='setparam'),
    path('params/get/<str:session>/<str:key>', views.view_get_param, name='getparam'),
    ]