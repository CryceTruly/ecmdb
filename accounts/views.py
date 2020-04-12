from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def register(self):
    pass


def login(request):
    if request.method == "POST":
        context = {"values": request.POST}
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(email=username, password=password).first()
        if user is not None:
            auth.login(request, user)
            messages.success(request,  'Welcome  ' +
                             user.email+'  you are now logged in')
            if user.role == 'ACCOUNTANT':
                return redirect('expenses')
            if user.role == 'TECHNICIAN':
                return redirect('reports')
            if user.role == 'BOSS':
                return redirect('reports')

        messages.error(request,  'Invalid credentials')
        return render(request, 'accounts/login.html',
                      context)

    return render(request, "accounts/login.html")


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request,  'You are now logged out')
        return redirect('index')
    return render(request, "accounts/login.html")


@login_required(login_url='/accounts/login')
def accounts(request):
    context = {
        "expenses": []
    }
    return render(request, "accounts/accounts.html", context)


@login_required(login_url='/accounts/login')
def technician(request):
    context = {
        "reports": []
    }
    return render(request, "accounts/technician.html", context)


def boss(request):
    context = {
        'reports': []
    }
    return render(request, "accounts/boss.html", context)
