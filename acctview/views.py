import json

from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, redirect
from decouple import config
from home.usersettings import UserSettings
from django.contrib.auth.decorators import login_required
import requests
from usergroups import UserGroups


# Create your views here.
def acctview_home(request):
    return render(request, 'acctview_home.html')


@login_required
def accounts(request):
    context = {}
    api_data = []
    search_term = ''
    show_account_chk = 'off'

    if UserGroups(request).not_user:
        return redirect(reverse('not-authorized'))

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

    if UserGroups(request).not_user:
        return redirect(reverse('not-authorized'))

    if account is None:
        url = reverse('accounts')
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

    url = config('API_URL') + 'account/balance/' + account

    balance_data = []

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        balance_data = rawdata['data']

    context['balance'] = balance_data.copy()

    url = config('API_URL') + 'account/transactions/' + account

    transaction_data = []

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        transaction_data = rawdata['data']

    # sort transactions by date ascending, then by code_id ascending
    transaction_data.sort(key=lambda x: (x['trandate'], x['code_id']))

    context['transactions'] = transaction_data.copy()

    return render(request, 'account_wells.html', context=context)


@login_required
def acct_graph_disp(request):
    def not_empty(value):
        if value is None or value == '' or value.lower() == 'none':
            return False
        else:
            return True

    def build_account_name(data):
        return data['name']

    # ref: https://chat.openai.com/share/9a5259a7-709e-4538-9a9e-405baf89a6d2
    account = request.GET.get('account', None)
    months = request.GET.get('months', None)
    show_wells = request.GET.get('show_wells', None)

    if UserGroups(request).not_user:
        return redirect(reverse('not-authorized'))

    if account is None:
        url = reverse('accounts')
        return redirect(url)

    context = {}
    context['account'] = account

    api_data = []

    url = config('API_URL') + 'account/one/' + account

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        api_data = rawdata['data']

    context['account'] = build_account_name(api_data)
    context['account_id'] = account

    api_data = []

    # Get graph data
    url = config('API_URL') + 'account/well-graph-data?account=' + account
    if not (show_wells is None):
        url = url + '&show_wells=' + show_wells
    if not (months is None):
        url = url + '&months=' + months

    if show_wells is None:
        context['show_wells'] = True
    else:
        if show_wells == '1':
            context['show_wells'] = True
        else:
            context['show_wells'] = False

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        api_data = rawdata['data']

    if context['show_wells']:
        # sort by yearmonth, then by well_id
        api_data.sort(key=lambda x: (x['yearmonth'], x['well_id']))
    else:
        # sort by yearmonth
        api_data.sort(key=lambda x: x['yearmonth'])

    # add labels for graph
    for d in api_data:
        if context['show_wells']:
            d['label'] = d['yearmonth'] + ' ' + d['well_id']
        else:
            d['label'] = d['yearmonth']

    # Reformat data for graph
    # Create list of unique yearmonths
    yearmonths = []
    for d in api_data:
        if d['yearmonth'] not in yearmonths:
            yearmonths.append(d['yearmonth'])

    well_ids = []
    for d in api_data:
        if d['well_id'] not in well_ids:
            well_ids.append(d['well_id'])

    # now create a list of yearmonths, and for each yearmonth, create a list of well_id and acft
    graph_data = []
    for ym in yearmonths:
        graph_data.append({'yearmonth': ym, 'data': []})
        for d in api_data:
            if d['yearmonth'] == ym:
                graph_data[-1]['data'].append({'well_id': d['well_id'], 'acft': d['acft']})

    context['graph_data'] = json.dumps(graph_data.copy())
    context['yearmonths'] = json.dumps(yearmonths.copy())
    context['well_ids'] = json.dumps(well_ids.copy())

    return render(request, 'well_graph.html', context=context)

