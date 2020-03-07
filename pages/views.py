from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def index(request):
    return render(request, "pages/index.html", {})


@login_required(login_url='/accounts/login')
def about(request):

    context = {
    }
    return render(request, "pages/about.html", context)
