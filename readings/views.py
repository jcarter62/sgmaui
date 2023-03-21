from django.shortcuts import render
from decouple import config
import requests


# Create your views here.
def readings_home(request):
    return render(request, 'readings_home.html')

# create view for manual reading entry
def readings_manual(request):
    return render(request, 'readings_manual.html')

# view to display list of meters, and allow user to select one
def readings_ui(request):
    context = {}
    data = []

    url = config('API_URL') + 'reading/meters'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']

    record_count = data.__len__()

    context['wells'] = data
    context['record_count'] = record_count

    return render(request, 'readings_ui.html', context=context)
