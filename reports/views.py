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
from django.core.files.storage import FileSystemStorage
from reports.models import Comment


@login_required(login_url='/accounts/login')
def search_reports(request):
    data = request.body.decode('utf-8')
    search_val = json.loads(data).get('data')

    if request.user.role in ['BOSS', 'ACCOUNTANT']:
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
    if request.user.role == 'BOSS' or request.user.role == 'ACCOUNTANT':
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
    comments = Comment.objects.all()
    context = {
        'my_reports': reports,
        'page_obj': page_obj,
        'comments': comments
    }

    return render(request, 'reports/index.html', context)


@login_required(login_url='/accounts/login')
def add_report(request):
    banks = Bank.objects.all()

    context = {
        'banks': banks}
    if request.method == 'GET':
        return render(request, 'reports/add_report.html', context)
    if request.method == 'POST':
        banks = Bank.objects.all()
        has_error = False
        context = {
            'values': request.POST,
            'banks': banks
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
        report_file = request.FILES and request.FILES['report_file']
        if not report_file:
            messages.error(request,  'Please choose a report file document')
            has_error = True
        if not owner:
            messages.error(request,  'Asset Owner fullname is required')
            has_error = True
        if not purpose:
            messages.error(request,  'Purpose is required')
            has_error = True

        if not contact:
            has_error = True
            messages.error(request,  'Owner Contact is required')
        if contact and len(contact) is not 10:
            has_error = True
            messages.error(
                request,  'The Contact phone should be  10 characters')
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
                                        report_file=report_file,
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
    comments = Comment.objects.filter(report_id=id)
    return render(request, 'reports/report.html', {'report': report, 'comments': comments})


@login_required(login_url='/accounts/login')
def report_reciept(request, id):
    report = Report.objects.get(id=id)
    company = Company.objects.first()
    return render(request, 'reports/reciept.html', {'report': report, 'company': company})


@login_required(login_url='/accounts/login')
def report_edit(request, id):
    if request.method == 'GET':
        banks = Bank.objects.all()
        report = Report.objects.get(id=id)
        context = {
            'values': report,
            'banks': banks}
        return render(request, 'reports/edit-report.html', context)
    if request.method == 'POST':
        report = Report.objects.get(id=id)
        has_error = False
        context = {
            'values': request.POST,
            'banks': Bank.objects.all()
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
        report_file = request.FILES and request.FILES['report_file']
        if not owner:
            messages.error(request,  'Owner fullname is required')
            has_error = True
        if not purpose:
            messages.error(request,  'Purpose is required')
            has_error = True

        if not contact:
            has_error = True
            messages.error(request,  'Owner Contact is required')
        if contact and len(contact) is not 10:
            has_error = True
            messages.error(
                request,  'The Contact phone should be  10 characters')
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

            if report_file:
                report.report_file = report_file
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
            return redirect('report', report.pk)
        else:
            return redirect('report-edit', report.pk)

        return render(request, 'reports/edit-report.html', {'values': report})


@login_required(login_url='/accounts/login')
def report_approve(request, id):
    report = Report.objects.get(id=id)
    report.approved = True
    report.save()
    messages.success(request, 'Report Approved Successfully')
    return redirect('report', id)


@login_required(login_url='/accounts/login')
def add_report_comments(request, id):
    if request.method == 'GET':
        return render(request, 'reports/add_comment.html', {'id': id})
    if request.method == 'POST':
        has_error = False
        context = {
            'values': request.POST,
        }
        comment = request.POST['message']

    if not comment:
        has_error = True
        messages.error(request,  'Please add your comment')
    if has_error:
        return render(request, 'reports/add_comment.html', {'id': id})
    rep = Comment.objects.create(created_by=request.user,
                                 message=comment,
                                 report=Report.objects.get(id=id))

    if rep:
        messages.success(request, 'Comment added  Successfully')
        return redirect('report', id)


@login_required(login_url='/accounts/login')
def report_stats(request):
    today = Report.objects.filter(created_at='2020-03-11')
    context = {
        'today': 20000,
        'this_week': 200000,
        'this_month': 30000,
        'this_year': 400000000, 'all_time': 400000000000
    }
    return render(request, 'reports/stats.html', context)


def report_stats_rest(request):
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
