from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from decouple import config
import requests
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from .forms import WellAssocForm
from home.usersettings import UserSettings
from uuid import uuid4

# Create your views here.
def mw_home(request):
    return render(request, 'mw_home.html')

@login_required
def display_wells(request):
    context = {}
    data = []
    search_term = ''

    url = config('API_URL') + 'well-assoc/list_all'

    cookies = request.COOKIES.items()
    for item in cookies:
        if item[0] == 'search_term':
            search_term = item[1]

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        if search_term > '':
            for d in rawdata['data']:
                if search_term in d['well_id']:
                    data.append(d)
        else:
            data = rawdata['data']

    record_count = data.__len__()

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

#    page_size = request.COOKIES.get('page_size', 10)
    page_size = UserSettings(username=username).settings['rows_per_page']


    p = Paginator(data, page_size)
    page = request.GET.get('page', 1)
    wells = p.get_page(page)
    context['wells'] = wells
    context['record_count'] = record_count

    return render(request, 'display-wells.html', context=context)


@login_required
def display_well_details(request, well_id: str):
    context = {}
    data = []
    amount_hdr = 'Amount'

    url = config('API_URL') + 'well-assoc/one-well/' + well_id

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        data = rawdata['data']
        for d in data:
            d['begindate'] = d['begindate'][0:10]
            if d['enddate'] == 'None':
                d['enddate'] = ''
            else:
                d['enddate'] = d['enddate'][0:10]
            account = d['account']
            d['url'] = reverse(viewname='account_name', args=[account])

    amount_hdr = 'Amount'
    amount_alarm = False
    # calculate total amount
    total = 0.0
    for d in data:
        if d['isactive'] == '1':
            total += float(d['amount'])

    amount_hdr = 'Amount ({:.2f})'.format(total)
    if total > 100.01 or total < 99.99:
        amount_alarm = True
    else:
        amount_alarm = False

    record_count = data.__len__()

    page_size = request.COOKIES.get('page_size', 10)

    p = Paginator(data, page_size)
    page = request.GET.get('page', 1)
    well = p.get_page(page)
    context['well'] = well
    context['record_count'] = record_count
    context['well_id'] = well_id
    context['amount_hdr'] = amount_hdr
    context['amount_alarm'] = amount_alarm

    return render(request, 'display-well-details.html', context=context)


# implement post method to save well details
@login_required
def save_well_details(request):
    def generate_params(request) -> str:
        p = ''
        p += '?rec_id=' + request.POST.get('rec_id')
        p += '&well_id=' + request.POST.get('well_id')
        p += '&account=' + request.POST.get('account')
        p += '&amount=' + request.POST.get('amount')
        p += '&method=' + request.POST.get('method')
        p += '&begindate=' + request.POST.get('begindate')
        p += '&enddate=' + request.POST.get('enddate', None)
        p += '&ordering=' + request.POST.get('ordering')
        p += '&isactive=' + request.POST.get('isactive')
        p = p.replace(' ', '%20')
        return p

    well_id = request.POST.get('well_id')
    if request.method == 'POST':
        if request.POST.get('button') == 'Update':
            url = config('API_URL') + 'well-assoc/save-well-details' + generate_params(request)
            headers = {'Content-Type': 'application/json'}
            # response = requests.post(url=url, data=data)
            response = requests.post(url)
            if response.status_code == 200:
                # save "success" message
                pass
            else:
                print(response.message)
        elif request.POST.get('button') == 'Delete':
            url = config('API_URL') + 'well-assoc/delete-one-record' + '?rec_id=' + request.POST.get('rec_id')
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url)
            if response.status_code == 200:
                response.message = 'Record deleted'
            else:
                response.message = 'Record not deleted'
    else:
        pass

    redirect_url = reverse(viewname='display_well_details', args=[well_id])
    return redirect(redirect_url)


# 'reorder_well
@login_required
def reorder_well_records(request, well_id: str):
    url = config('API_URL') + f'well-assoc/reorder-well-records/{well_id}'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url)
    if response.status_code == 200:
        pass
    else:
        print(response.message)

    redirect_url = reverse(viewname='display_well_details', args=[well_id])
    return redirect(redirect_url)


# add_well_assoc_record
@login_required
def add_well_assoc_record(request, well_id: str):
    def generate_short_guid() -> str:
        x = str(uuid4())
        x = x.replace('-', '').lower()
        return x

    # method to generate todays date in form of yyyy-mm-dd
    def generate_todays_date() -> str:
        from datetime import date
        today = date.today()
        return today.strftime("%Y-%m-%d")

    form = WellAssocForm(initial={
        'rec_id': generate_short_guid(),
        'well_id': well_id,
        'account': '0',
        'amount': 0,
        'method': 'PCT',
        'begindate': generate_todays_date(),
        'enddate': None,
        'ordering': 99,
        'isactive': '1',
    })
    if request.method == 'POST':
        form = WellAssocForm(request.POST)
        if form.is_valid():
            form.save()
            redirecturl = reverse(viewname='display_well_details', args=[well_id])
            return redirect(redirecturl)

    context = {'form': form}

    return render(request, 'add-well-assoc-record.html', context=context)
    return
