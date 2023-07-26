from django.http import JsonResponse
from decouple import config
import requests
from http import HTTPStatus


# return json data for parcel details
def account_name(request, account: int):
    code = HTTPStatus.OK
    result = {}
    # /well-assoc/account-name/4410'
    url = config('API_URL') + f'well-assoc/account-name/{account}'
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300:
        code = response.status_code
        data = response.json()
        result['message'] = data[0]['message']
        if data[0]['data'] == '':
            code = HTTPStatus.NO_CONTENT
        else:
            for fld in data[0]['data']:
                result[fld] = data[0]['data'][fld]
    else:
        result['message'] = "error"
        code = HTTPStatus.INTERNAL_SERVER_ERROR

    # return json data
    # ref: https://koenwoortman.com/python-django-view-return-json-response/
    return JsonResponse(result, status=code)


def account_details(request, account: int):
    data = {}
    code = HTTPStatus.OK
    # /well-assoc/account-details/4410'
    url = config('API_URL') + f'well-assoc/account-details/{account}'
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300:
        code = response.status_code
        data = response.json()[0]['data']
        if data == '':
            data = {}
            code = HTTPStatus.NO_CONTENT
        data['message'] = "success"
    else:
        data['message'] = "error"
        code = HTTPStatus.INTERNAL_SERVER_ERROR

    # return json data
    # ref: https://koenwoortman.com/python-django-view-return-json-response/
    return JsonResponse(data, status=code)


def well_details(request, well_id: str):
    '''Return json data for well details'''
    data = {}
    code = HTTPStatus.OK
    # /well-assoc/well-details/4410'
    url = config('API_URL') + f'well-assoc/well-details/{well_id}'
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300:
        code = response.status_code
        data = response.json()[0]['data']
        if data == '':
            data = {}
            code = HTTPStatus.NO_CONTENT
        data['message'] = "success"
    else:
        data['message'] = "error"
        code = HTTPStatus.INTERNAL_SERVER_ERROR

    # return json data
    # ref: https://koenwoortman.com/python-django-view-return-json-response/
    return JsonResponse(data, status=code)


def account_well_count(request, account: int):
    data = {}
    code = HTTPStatus.OK
    # /account/wells/4410'
    url = config('API_URL') + f'account/wells/{account}'
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300:
        code = response.status_code
        data = response.json()['data']
        if data == '':
            data = {
                "well_count": 0,
                "message": "success",
            }
            code = HTTPStatus.NO_CONTENT
        else:
            data = {
                "well_count": data.__len__(),
                "message": "success",
            }
    else:
        data = {
            "well_count": 0,
            "message": "error",
        }
        code = HTTPStatus.INTERNAL_SERVER_ERROR


    # return json data
    # ref: https://koenwoortman.com/python-django-view-return-json-response/
    return JsonResponse(data, status=code)


# views.well_readings, name='well_readings'),
def well_readings(request, well_id: str):
    result = {}
    code = HTTPStatus.OK
    # /reading/lastyear/well_id'
    url = config('API_URL') + f'reading/lastyear/{well_id}'
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300:
        code = response.status_code
        data = response.json()['data']
        if data == '':
            code = HTTPStatus.NO_CONTENT
        result['message'] = "success"
    else:
        result['message'] = "error"
        code = HTTPStatus.INTERNAL_SERVER_ERROR

    result['well_id'] = well_id
    result['data'] = data
    # return json data
    # ref: https://koenwoortman.com/python-django-view-return-json-response/
    return JsonResponse(result, status=code)


# views.well_last_reading, name='well_last_reading'),
def well_last_reading(request, well_id: str):
    result = {}
    code = HTTPStatus.OK
    # /reading/lastyear/well_id'
    url = config('API_URL') + f'reading/last/{well_id}'
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300:
        code = response.status_code
        data = response.json()['data']
        if data == '':
            code = HTTPStatus.NO_CONTENT
        result['message'] = "success"
    else:
        result['message'] = "error"
        code = HTTPStatus.INTERNAL_SERVER_ERROR

    result['well_id'] = well_id
    result['data'] = data
    # return json data
    # ref: https://koenwoortman.com/python-django-view-return-json-response/
    return JsonResponse(result, status=code)

# views.add_reading, name='add_reading'),
def add_reading(request, params):
    # well_id, reading, operator, read_date, read_time, note):
    url = config('API_URL') + f'reading/add?params={params}'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        response.message = 'Record Added'
    else:
        response.message = 'Record Add Failed'

    return JsonResponse(response.json(), status=response.status_code)
