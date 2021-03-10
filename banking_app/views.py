from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'banking_app/index.html', context)