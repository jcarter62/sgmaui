from django.shortcuts import render

# Create your views here.
def wa_home(request):
    return render(request, 'wa_home.html')

