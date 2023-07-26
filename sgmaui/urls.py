"""sgmaui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from decouple import config

urlpatterns = [

    path('', include('home.urls'), name='home'),
    path('authenticate/', include('authenticate.urls')),

    path('mp/', include('mtnparcel.urls')),
    path('ar/', include('allocreq.urls')),
    path('mw/', include('mtnwell.urls')),
    path('wa/', include('wellassoc.urls')),
    path('imd/', include('impmtrdata.urls')),
    path('au/', include('applyuse.urls')),
    path('misc/', include('misc.urls')),
    path('acctview/', include('acctview.urls')),
    path('readings/', include('readings.urls')),
    path('admin/', admin.site.urls),

]

try:
    orgname = config('ORGANIZATION_NAME', default='')
except:
    orgname = ''

admin.site.site_header = orgname
admin.site.site_title = orgname
admin.site.index_title = orgname
