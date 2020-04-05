from django.shortcuts import render, redirect, get_object_or_404
from banks.models import Bank
from django.contrib import messages
from .models import Report
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.db.models import Q
from company.models import Company


@login_required(login_url='/accounts/login')
def search_reports(request):
    data = request.body.decode('utf-8')
    search_val = json.loads(data).get('data')

    if(request.user.role == 'BOSS'):
        reports = Report.objects.filter(plot_no__icontains=search_val) | Report.objects.filter(
            location__startswith=search_val) | Report.objects.filter(
            owner__icontains=search_val) | Report.objects.filter(
            purpose__icontains=search_val) | Report.objects.filter(
            client__icontains=search_val) | Report.objects.filter(
            delivery_date__icontains=search_val) | Report.objects.filter(
            contact__icontains=search_val) | Report.objects.filter(
            created_by__email__icontains=search_val)
        data = list(reports.values())
        return JsonResponse(data, safe=False)
    if(request.user.role == 'TECHNICIAN'):
        reports = Report.objects.filter(plot_no__icontains=search_val, created_by=request.user) | Report.objects.filter(
            location__startswith=search_val, created_by=request.user) | Report.objects.filter(
            owner__icontains=search_val, created_by=request.user) | Report.objects.filter(
            purpose__icontains=search_val, created_by=request.user) | Report.objects.filter(
            client__icontains=search_val, created_by=request.user) | Report.objects.filter(
            delivery_date__icontains=search_val, created_by=request.user) | Report.objects.filter(
            contact__icontains=search_val, created_by=request.user) | Report.objects.filter(
            created_by__email__icontains=search_val, created_by=request.user)
        data = list(reports.values())
        return JsonResponse(data, safe=False)


@login_required(login_url='/accounts/login')
def index(request):
    if request.user.role == 'BOSS':
        reports = Report.objects.all().order_by('approved')
        paginator = Paginator(reports, 7)  # Show 7 items per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'reports': reports,
            'page_obj': page_obj
        }
        return render(request, 'reports/all_reports.html', context)
    reports = Report.objects.filter(created_by=request.user)
    paginator = Paginator(reports, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'my_reports': reports,
        'page_obj': page_obj
    }
    return render(request, 'reports/index.html', context)


@login_required(login_url='/accounts/login')
def add_report(request):
    if request.method == 'GET':
        return render(request, 'reports/add_report.html')
    if request.method == 'POST':
        has_error = False
        context = {
            'values': request.POST
        }
        owner = request.POST['owner']
        contact = request.POST['contact']
        location = request.POST['location']
        plot_no = request.POST['plot_no']
        inspection_date = request.POST['inspection_date']
        delivery_date = request.POST['delivery_date']
        amount = request.POST['amount']
        purpose = request.POST['purpose']
        bank = request.POST['bank']
        if not owner:
            messages.error(request,  'Asset Owner fullname is required')
            has_error = True
        if not purpose:
            messages.error(request,  'Purpose is required')
            has_error = True

        if not contact:
            has_error = True
            messages.error(request,  'Owner Contact is required')
        if not location:
            has_error = True
            messages.error(request,  'Location is required')

        if not plot_no:
            has_error = True
            messages.error(request,  'Plot Number is required')
        if not inspection_date:
            has_error = True
            messages.error(request,  'Inspection Date is required')
        if not delivery_date:
            has_error = True
            messages.error(request,  'Delivery Date  is required')
        if not amount:
            has_error = True
            messages.error(request,  'Amount Paid is required')
        if not bank:
            has_error = True
            messages.error(request,  'Client Bank is required')

        if not has_error:
            num_results = Report.objects.filter(
                plot_no=request.POST['plot_no'].upper()).count()
            if num_results > 0:
                has_error = True
                messages.error(request,  'Report with this plot number Exists')
                return render(request, 'reports/add_report.html', context)
        if not has_error:
            rep = Report.objects.create(created_by=request.user,
                                        owner=owner,
                                        location=location,
                                        amount=amount,
                                        client=bank,
                                        purpose=purpose,
                                        contact=contact,
                                        plot_no=plot_no.upper(),
                                        inspection_date=inspection_date,
                                        delivery_date=delivery_date,
                                        report_payed_for=True,
                                        reason_for_not_paying='N/A')

            if rep:
                messages.success(request, 'Report Submitted Successfully')
                return redirect('reports')

        return render(request, 'reports/add_report.html', context)


@login_required(login_url='/accounts/login')
def report(request, id):
    report = Report.objects.get(id=id)
    return render(request, 'reports/report.html', {'report': report})


@login_required(login_url='/accounts/login')
def report_reciept(request, id):
    report = Report.objects.get(id=id)
    company = Company.objects.first()
    return render(request, 'reports/reciept.html', {'report': report, 'company': company})


@login_required(login_url='/accounts/login')
def report_edit(request, id):

    if request.method == 'GET':
        report = Report.objects.get(id=id)
        return render(request, 'reports/edit-report.html', {'values': report})
    if request.method == 'POST':
        report = Report.objects.get(id=id)

        has_error = False
        context = {
            'values': request.POST
        }
        owner = request.POST['owner']
        contact = request.POST['contact']
        location = request.POST['location']
        plot_no = request.POST['plot_no']
        inspection_date = request.POST['inspection_date']
        delivery_date = request.POST['delivery_date']
        amount = request.POST['amount']
        purpose = request.POST['purpose']
        bank = request.POST['bank']

        if not owner:
            messages.error(request,  'Owner fullname is required')
            has_error = True
        if not purpose:
            messages.error(request,  'Purpose is required')
            has_error = True

        if not contact:
            has_error = True
            messages.error(request,  'Owner Contact is required')
        if not location:
            has_error = True
            messages.error(request,  'Location is required')

        if not plot_no:
            has_error = True
            messages.error(request,  'Plot Number is required')
        if not inspection_date:
            has_error = True
            messages.error(request,  'Inspection Date is required')
        if not delivery_date:
            has_error = True
            messages.error(request,  'Delivery Date  is required')
        if not amount:
            has_error = True
            messages.error(request,  'Amount Paid is required')
        if not bank:
            has_error = True
            messages.error(request,  'Client Bank is required')
        if not has_error:
            report = Report.objects.get(id=id)
            report.location = location
            report. amount = amount
            report.client = bank
            report.purpose = purpose
            report.owner = owner
            report.contact = contact
            report.plot_no = plot_no
            report.inspection_date = inspection_date
            report.delivery_date = delivery_date
            report.report_payed_for = True
            report.reason_for_not_paying = 'N/A'
            report.save()
            messages.success(request, 'Report Updated Successfully')
            return redirect('report', id)
        else:
            return render(request, 'reports/edit-report.html',  context)

        return render(request, 'reports/edit-report.html', {'values': report})


@login_required(login_url='/accounts/login')
def report_approve(request, id):
    report = Report.objects.get(id=id)
    report.approved = True
    report.save()
    messages.success(request, 'Report Approved Successfully')
    return redirect('report', id)
