from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, redirect
from decouple import config
from home.usersettings import UserSettings
from django.contrib.auth.decorators import login_required
import requests


# Create your views here.
@login_required
def gw_input_params(request):
    context = {}
    search_term = ''
    show_account_chk = 'off'
    from_date = '03/01/2023'
    to_date = ''
    calc_date = ''
    tc_code = ''
    code_code = ''

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    cookies = request.COOKIES.items()
    for item in cookies:
        if item[0] == 'gc_from_date':
            from_date = item[1]
        if item[0] == 'gc_to_date':
            to_date = item[1]
        if item[0] == 'gc_calc_date':
            calc_date = item[1]
        if item[0] == 'gc_tc_code':
            tc_code = item[1]
        if item[0] == 'gc_code_code':
            code_code = item[1]

    context = {
        "title": "Groundwater Calculation Input",

        "from_date": from_date,
        "to_date": to_date,
        "calc_date": calc_date,
        "tc_code": tc_code,
        "code_code": code_code,
        "results": {},
    }


    #
    # handle post request
    if request.method == 'POST':
        # if button value is 'viewresults' then redirect to gwcalc_results
        if request.POST['action'] == 'view':
            return redirect(reverse('gw_view_calc_results'))

        if 'gc_from_date' in request.POST:
            from_date = request.POST['gc_from_date']
        if 'gc_to_date' in request.POST:
            to_date = request.POST['gc_to_date']
        if 'gc_calc_date' in request.POST:
            calc_date = request.POST['gc_calc_date']
        if 'gc_tc_code' in request.POST:
            tc_code = request.POST['gc_tc_code']
        if 'gc_code_code' in request.POST:
            code_code = request.POST['gc_code_code']

        # now we need to calculate.

        url = config('API_URL') + 'gwcalc/calc/' + from_date + '/' + to_date + '/' + \
              calc_date + '/' + tc_code + '/' + code_code + '/0'

        calc_data = []

        response = requests.get(url)
        if response.status_code == 200:
            rawdata = response.json()
            calc_data = rawdata['data']

        context['results'] = calc_data.copy()

    else:
        url = config('API_URL') + 'gwcalc/calc_status'

        calc_data = []

        response = requests.get(url)
        if response.status_code == 200:
            rawdata = response.json()
            calc_data = rawdata['data']

        context['results'] = calc_data.copy()


    return render(request, 'gwcalc_inputs.html', context=context)


@login_required
def gw_view_calc_results(request):
    context = {}
    search_term = ''
    filter_txt = ''

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    cookies = request.COOKIES.items()
    for item in cookies:
        if item[0] == 'search_term':
            search_term = item[1]

    context = {
        "title": "Groundwater Calculation Results",
        "results": {},
        "filter": filter_txt,
    }
    # handle post request
    url = config('API_URL') + 'gwcalc/calc_results'

    calc_data = []

    response = requests.get(url)
    if response.status_code == 200:
        rawdata = response.json()
        if search_term > '':
            filter_txt = '- Filtered by: ' + search_term
            for item in rawdata['data']:
                txt = item['description'] + ' ' + item['memo'] + ' ' + item['name_id']
                if search_term in txt:
                    calc_data.append(item)
        else:
            filter_txt = ''
            calc_data = rawdata['data']

    context['results'] = calc_data.copy()
    context['filter'] = filter_txt
    #
    # calculate total amount.
    total_qty = 0
    transaction_count = 0
    account_count = 0
    current_account = 0
    for item in calc_data:
        total_qty = total_qty + float(item['amount'])
        transaction_count = transaction_count + 1
        if item['name_id'] != current_account:
            current_account = item['name_id']
            account_count = account_count + 1


    context['total_qty'] = total_qty
    context['transaction_count'] = transaction_count
    context['account_count'] = account_count

    return render(request, 'view_calc_results.html', context=context)


