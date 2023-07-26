from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
from django.core.paginator import Paginator
from django.http import JsonResponse
from decouple import config
from home.usersettings import UserSettings

# Create your views here.
def mp_home(request):
    return render(request, 'mp_home.html')


# pagination reference:
# https://youtu.be/N-PB-HMFmdo
#
@login_required
def mp_parcels(request):
    context = {}
    data = []
    search_term = ''


    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    page_size = UserSettings(username=username).settings['rows_per_page']
    show_only_active_parcels = \
        ( UserSettings(username=username).settings['show_only_active_parcels'] == 'True')

    cookies = request.COOKIES.items()
    for item in cookies:
        if item[0] == 'search_term':
            search_term = item[1]

    url = config('API_URL') + 'parcel/list'
    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        data1 = []
        if show_only_active_parcels:
            for d in rawdata['data']:
                if d['isactive'] == 1:
                    data1.append(d)
        else:
            data1 = rawdata['data']

        if search_term > '':
            for d in data1:
                if search_term in d['parcel_id']:
                    data.append(d['parcel_id'])
        else:
            for d in data1:
                data.append(d['parcel_id'])

    record_count = data.__len__()

    # page_size = request.COOKIES.get('page_size', 10)

    p = Paginator(data, page_size)
    page = request.GET.get('page', 1)
    parcels = p.get_page(page)
    context['parcels'] = parcels
    context['record_count'] = record_count

    return render(request, 'mp_parcels.html', context=context)


# return json data for parcel details
def mp_parcel_details(request, parcel_id):
    context = {}
    data = None
    url = config('API_URL') + f'parcel/details/{parcel_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        context['parcel'] = data

    # return json data
    # ref: https://koenwoortman.com/python-django-view-return-json-response/
    return JsonResponse(data)
