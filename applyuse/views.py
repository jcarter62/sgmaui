from django.shortcuts import render

# Create your views here.
def au_home(request):
    return render(request, 'au_home.html')


