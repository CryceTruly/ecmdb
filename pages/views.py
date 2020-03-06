from django.shortcuts import render
from realtors.models import Realtor

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def index(request):
    return render(request, "pages/index.html", {})


@login_required(login_url='/accounts/login')
def about(request):
    realtors = Realtor.objects.order_by('-hire_date')

    mvp_realtors = Realtor.objects.filter(is_mvp=True)

    context = {
        "realtors": realtors,
        "mvp_realtors": mvp_realtors
    }
    return render(request, "pages/about.html", context)
