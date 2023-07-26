from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, redirect
from decouple import config
from home.usersettings import UserSettings
from django.contrib.auth.decorators import login_required
import requests


# Create your views here.
def acctview_home(request):
    return render(request, 'acctview_home.html')


@login_required
def accounts(request):
    context = {}
    api_data = []
    search_term = ''
    show_account_chk = 'off'

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    url = config('API_URL') + 'account/all'

    cookies = request.COOKIES.items()
    for item in cookies:
        if item[0] == 'search_term':
            search_term = item[1]
        if item[0] == 'show_account_chk':
            show_account_chk = item[1]


    if search_term > '':
        sep = '&' if url.find('?') > 0 else '?'
        url = url + sep + 'search_term=' + search_term

    if show_account_chk == 'on':
        sep = '&' if url.find('?') > 0 else '?'
        url = url + sep + 'accounts_with_well=1'

    # TODO: update api to accept query string "show_only_well_accounts" and return only accounts with wells

    print('api url: ' + url)

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        api_data = rawdata['data']

    record_count = api_data.__len__()

    page_size = UserSettings(username=username).settings['rows_per_page']

    p = Paginator(api_data, page_size)
    page = request.GET.get('page', 1)
    accounts = p.get_page(page)
    context['data'] = accounts
    context['record_count'] = record_count
    if show_account_chk == 'on':
        context['show_account_chk'] = True
    else:
        context['show_account_chk'] = False

    return render(request, 'accounts.html', context=context)


@login_required
def account_wells(request, account: str = None):

    def not_empty(value):
        if value is None or value == '' or value.lower() == 'none':
            return False
        else:
            return True

    def build_address_rows(data):
        address_rows = []
        address_rows.append(data['name'])
        if data['address1'] > '':
            address_rows.append(data['address1'])
        if not_empty(data['address2']):
            address_rows.append(data['address2'])
        if not_empty(data['address3']):
            address_rows.append(data['address3'])
        address_rows.append(data['city'] + ', ' + data['state'] + ' ' + data['zip'])
        if data['isactive'] == '1':
            address_rows.append('Account is Active')
        else:
            address_rows.append('Account is Inactive')
        return address_rows

    if account is None:
        url = reverse('acccounts')
        return redirect(url)


    context = {}
    context['account'] = account

    api_data = []

    url = config('API_URL') + 'account/one/' + account

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        api_data = rawdata['data']

    context['account'] = build_address_rows(api_data).copy()
    context['account_id'] = account

    api_data = []

    url = config('API_URL') + 'account/wells/' + account

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        api_data = rawdata['data']

    # change dates from datetime to only date
    for d in api_data:
        d['begindate'] = d['begindate'].split(' ')[0]
        if d['enddate'] == 'None':
            d['enddate'] = ''
        else:
            d['enddate'] = d['enddate'].split(' ')[0]

    context['wells'] = api_data.copy()

    return render(request, 'account_wells.html', context=context)

