from django.shortcuts import render
from banks.models import Bank

# Create your views here.


def index(request):
    return render(request, 'reports/index.html')


def add_report(request):
    return render(request, 'reports/add_report.html')
