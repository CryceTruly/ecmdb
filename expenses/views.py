from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


@login_required(login_url='/accounts/login')
def expenses(request):

    if request.user.role == 'TECHNICIAN':
        expenses = Expense.objects.filter(
            requester=request.user).order_by('-updated_at')
        context = {
            'expenses': expenses
        }
        return render(request=request, template_name='expenses/index.html', context=context)

    if request.user.role == 'ACCOUNTANT':
        expenses = Expense.objects.all()
        context = {
            'expenses': expenses
        }
        return render(request=request, template_name='expenses/all_expenses.html', context=context)


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
            amount=amount, purpose=purpose, requester=request.user, status='APPROVED')
    else:
        expense = Expense.objects.create(
            amount=amount, purpose=purpose, requester=request.user)

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
def expense_detail(request):
    expenses = Expense.objects.all()
    context = {
        'expenses': expenses
    }
    return render('expenses/index.html', context)


@login_required(login_url='/accounts/login')
def approve_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.status = 'APPROVED'
    expense.save()
    messages.success(request, 'Request approved')
    return redirect('expenses')
