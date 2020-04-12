from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import ExpenseFilter
from django.http import JsonResponse
import json


@login_required(login_url='/accounts/login')
def search_expenses(request):
    data = request.body.decode('utf-8')
    search_val = json.loads(data).get('data')

    if request.user.role == 'TECHNICIAN':
        expenses = Expense.objects.filter(purpose__icontains=search_val, requester=request.user) | Expense.objects.filter(
            amount__startswith=search_val, requester=request.user) | Expense.objects.filter(
            requested_on__icontains=search_val, requester=request.user) | Expense.objects.filter(
            status__icontains=search_val, requester=request.user) | Expense.objects.filter(
            submitted_by_name__icontains=search_val, requester=request.user)
        data = list(expenses.values())
        return JsonResponse(data, safe=False)

    expenses = Expense.objects.filter(purpose__icontains=search_val) | Expense.objects.filter(
        amount__startswith=search_val) | Expense.objects.filter(
        requested_on__icontains=search_val) | Expense.objects.filter(
        status__icontains=search_val) | Expense.objects.filter(
        submitted_by_name__icontains=search_val)
    data = list(expenses.values())
    return JsonResponse(data, safe=False)


@login_required(login_url='/accounts/login')
def expenses(request):

    if request.user.role == 'TECHNICIAN':
        expenses = Expense.objects.filter(
            requester=request.user).order_by('-updated_at')
        paginator = Paginator(expenses, 7)  # Show 7 items per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'expenses': expenses,
            'page_obj': page_obj
        }
        return render(request=request, template_name='expenses/index.html', context=context)

    if request.user.role == 'ACCOUNTANT':
        expenses = Expense.objects.all()
        expense_filter = ExpenseFilter(request.GET, queryset=expenses)

        paginator = Paginator(expenses, 7)  # Show 7 items per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'expenses': expenses,
            'page_obj': page_obj,
            'filter': expense_filter
        }
        return render(request=request, template_name='expenses/all_expenses.html', context=context)

    if request.user.role == 'BOSS':
        expenses = Expense.objects.all()
        paginator = Paginator(expenses, 7)  # Show 7 items per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'expenses': expenses,
            'page_obj': page_obj
        }
        return render(request=request, template_name='expenses/admin_all_expenses.html', context=context)


@login_required(login_url='/accounts/login')
def expenses_add(request):
    if request.method == 'GET':
        return render(request, 'expenses/new.html')
    amount = request.POST['amount']
    purpose = request.POST['purpose']
    if not amount:
        messages.error(request,  'Amount is required')
        return redirect('expenses')
    if not purpose:
        messages.error(request,  'Reason for the request is required')
        return redirect('expenses')

    expense = None

    if request.user.role == 'ACCOUNTANT':
        expense = Expense.objects.create(
            amount=amount, purpose=purpose, requester=request.user, status='APPROVED', submitted_by_name=request.user.email)
    else:
        expense = Expense.objects.create(
            amount=amount, purpose=purpose, requester=request.user, submitted_by_name=request.user.email)

    if expense:
        messages.success(request,  'Request was submitted successfully')
        return redirect('expenses')

    if expense:
        messages.success(request,  'Request was submitted successfully')
        return redirect('expenses')

    return render(request=request, template_name='expenses/index.html')


@login_required(login_url='/accounts/login')
def expense_edit(request, id):
    if request.method == 'GET':
        return render(request, 'expenses/index.html')
    amount = request.POST['amount']
    purpose = request.POST['purpose']
    if not amount:
        messages.error(request,  'Amount is required')
        return redirect('expenses')
    if not purpose:
        messages.error(request,  'Reason for the request is required')
        return redirect('expenses')
    expense = Expense.objects.get(id=id)
    expense.amount = amount
    expense.purpose = purpose
    expense.save()

    messages.success(request,  'Expense updated successfully')
    return redirect('expenses')


@login_required(login_url='/accounts/login')
def expense_delete(request):
    expenses = Expense.objects.all()
    context = {
        'expenses': expenses
    }
    return render('expenses/index.html', context)


@login_required(login_url='/accounts/login')
def expense_summary(request):
    today = Expense.objects.filter(approval_date='2020-03-11')
    context = {
        'today': 20000,
        'this_week': 200000,
        'this_month': 30000,
        'this_year': 400000000, 'all_time': 400000000000
    }
    return render(request, 'expenses/summary.html', context)


def expense_summary_rest(request):
    months = {
        "Jan": 30000,
        "Feb": 40000,
        "Mar": 50000,
        "Apr": 40000,
        "May": 50000,
        "Jun": 50000,
        "Jul": 50000,
        "Aug": 50000,
        "Sept": 50000,
        "Nov": 50000,
        "Dec": 50000
    }
    days = {
        "Mon": 30000,
        "Tue": 40000,
        "Wed": 50000,
        "Thur": 40000,
        "Fri": 50000,
        "Sat": 50000,
        "Sun": 50000,
    }
    data = {"months": months, "days": days}
    return JsonResponse({'data': data}, safe=False)


@login_required(login_url='/accounts/login')
def expense_detail(request):
    expenses = Expense.objects.all()
    context = {
        'expenses': expenses
    }
    return render('expenses/index.html', context)


@login_required(login_url='/accounts/login')
def approve_expense(request, id):
    expense = Expense.objects.get(id=id)
    if expense.status == 'APPROVED':
        expense.status = 'PENDING'
    else:
        expense.status = 'APPROVED'
    expense.save()
    messages.success(request, 'Expense  status updated')
    return redirect('expenses')
