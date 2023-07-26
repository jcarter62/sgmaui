from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from decouple import config
import requests

from home.usersettings import UserSettings


# Create your views here.
def readings_home(request):
    return render(request, 'readings_home.html')


# create view for manual reading entry
def readings_manual(request):
    # load list of wells and status.
    context = {}
    data = []

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    cookies = request.COOKIES.items()
    search_term = ''
    for item in cookies:
        if item[0] == 'search_term':
            search_term = item[1]


    url = config('API_URL') + 'reading/well-status'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']

    if search_term > '':
        data = [item for item in data if search_term in item['well_id']]

    record_count = data.__len__()

    page_size = UserSettings(username=username).settings['rows_per_page']

    p = Paginator(data, page_size)
    page = request.GET.get('page', 1)
    wells = p.get_page(page)
    context['data'] = wells
    context['record_count'] = record_count

    return render(request, 'readings_manual.html', context=context)


# view to display list of meters, and allow user to select one
@login_required
def readings_ui(request):
    from home.views import view_get_param
    context = {}
    data = []
    sessionid = ''

    if request.GET.get('clr', '0') != '0':
        clr = True
    else:
        clr = False

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    search_term = ''
    cookies = request.COOKIES.items()
    for item in cookies:
        if item[0] == 'search_term':
            search_term = item[1]
        if item[0] == 'id':
            sessionid = item[1]

    # load selected meter from session if it exists
    selected_meter = ''
    try:
        import json
        jsondata = view_get_param(request, sessionid, 'selected_meter')
        content = json.loads(jsondata.content)
        status = content['code']
        if status == 200:
            selected_meter = content['result']
    except:
        pass

    url = config('API_URL') + 'reading/meters'

    response = requests.get(url)
    if response.status_code == 200:
        data1 = response.json()['data']

    if search_term > '':
        data = [item for item in data1 if search_term in item['well_id']]
    else:
        data = data1

    record_count = data.__len__()

    page_size = UserSettings(username=username).settings['rows_per_page']

    p = Paginator(data, page_size)

    if clr:
        page = request.GET.get('page', 1)
    else:
        if selected_meter > '':
            page = 1
            for item in data:
                if item['well_id'] == selected_meter:
                    page = data.index(item) // int(page_size) + 1
                    break
        else:
            page = request.GET.get('page', 1)

    wells = p.get_page(page)
    context['data'] = wells
    context['record_count'] = record_count

    return render(request, 'readings_ui.html', context=context)
