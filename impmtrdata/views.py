from django.shortcuts import render

# Create your views here.
def imd_home(request):
    return render(request, 'imd_home.html')


