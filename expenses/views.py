from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import ExpenseFilter
from django.http import JsonResponse
import json
import datetime
import calendar
from django.contrib import auth


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
    if request.user.role == '':
        auth.logout(request)
        messages.warning(
            request, 'Your role is not authorized to access this area, please login again')
        return redirect('login')
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
    ex = Expense.objects.get(pk=id)
    if request.method == 'GET':
        return render(request, 'expenses/edit.html', {'ex': ex})
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
    expenses = Expense.objects.all_expenses()
    context = {
        'expenses': expenses
    }
    return render('expenses/index.html', context)


@login_required(login_url='/accounts/login')
def expense_summary(request):
    all_expenses = Expense.objects.filter(status='APPROVED')
    today = datetime.datetime.today().date()
    today2 = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    month_ago = today - datetime.timedelta(days=30)
    year_ago = today - datetime.timedelta(days=366)
    todays_amount = 0
    todays_count = 0
    this_week_amount = 0
    this_week_count = 0
    this_month_amount = 0
    this_month_count = 0
    this_year_amount = 0
    this_year_count = 0

    for one in all_expenses:
        if one.approved_at.date() == today:
            todays_amount += one.amount
            todays_count += 1

        if one.approved_at.date() >= week_ago:
            this_week_amount += one.amount
            this_week_count += 1

        if one.approved_at.date() >= month_ago:
            this_month_amount += one.amount
            this_month_count += 1

        if one.approved_at.date() >= year_ago:
            this_year_amount += one.amount
            this_year_count += 1

    context = {
        'today': {
            'amount': todays_amount,
            "count": todays_count,

        },
        'this_week': {
            'amount': this_week_amount,
            "count": this_week_count,

        },
        'this_month': {
            'amount': this_month_amount,
            "count": this_month_count,

        },
        'this_year': {
            'amount': this_year_amount,
            "count": this_year_count,

        },

    }
    return render(request, 'expenses/summary.html', context)


def expense_summary_rest(request):
    all_expenses = Expense.objects.filter(status='APPROVED')
    today = datetime.datetime.today().date()
    today_amount = 0
    months_data = {}
    week_days_data = {}

    def get_amount_for_month(month):
        month_amount = 0
        for one in all_expenses:
            month_, year = one.approved_at.month, one.approved_at.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        today_month, today_year = x, datetime.datetime.today().year
        for one in all_expenses:
            months_data[x] = get_amount_for_month(x)

    def get_amount_for_day(x, today_day, month, today_year):
        day_amount = 0
        for one in all_expenses:
            day_, date_,  month_, year_ = one.approved_at.isoweekday(
            ), one.approved_at.date().day, one.approved_at.month, one.approved_at.year
            if x == day_ and month == month_ and year_ == today_year:
                if not day_ > today_day:
                    day_amount += one.amount
        return day_amount

    for x in range(1, 8):
        today_day, today_month, today_year = datetime.datetime.today(
        ).isoweekday(), datetime.datetime.today(
        ).month, datetime.datetime.today().year
        for one in all_expenses:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {"months": months_data, "days": week_days_data}
    return JsonResponse({'data': data}, safe=False)


@login_required(login_url='/accounts/login')
def expense_detail(request):
    expenses = Expense.objects.all_expenses()
    context = {
        'expenses': expenses
    }
    return render('expenses/index.html', context)


@login_required(login_url='/accounts/login')
def approve_expense(request, id):
    expense = Expense.objects.get(id=id)
    if expense.status == 'APPROVED':
        expense.approved_at = None
        expense.status = 'PENDING'
    else:
        expense.status = 'APPROVED'
        expense.approved_at = datetime.datetime.now()

    expense.save()
    messages.success(request, 'Expense  status updated')
    return redirect('expenses')
