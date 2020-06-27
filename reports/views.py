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
import datetime

from django.http import JsonResponse, HttpResponse


from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib.sites.shortcuts import get_current_site


@login_required(login_url='/accounts/login')
def search_reports(request):
    data = request.body.decode('utf-8')
    search_val = json.loads(data).get('data')

    if request.user.role in ['BOSS', 'ACCOUNTANT']:
        reports = Report.objects.filter(upi__icontains=search_val) | Report.objects.filter(
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
        reports = Report.objects.filter(upi__icontains=search_val, created_by=request.user) | Report.objects.filter(
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
        upi = request.POST['upi']
        inspection_date = request.POST['inspection_date']
        delivery_date = request.POST['delivery_date']
        amount = request.POST['amount'] if request.POST['amount'] else 0
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
        if contact and len(contact) is not 10:
            has_error = True
            messages.error(
                request,  'The Contact phone should be  10 characters')

        if not upi:
            has_error = True
            messages.error(request,  'UPI is required')
        if not inspection_date:
            has_error = True
            messages.error(request,  'Inspection Date is required')
        if not delivery_date:
            has_error = True
            messages.error(request,  'Delivery Date  is required')
        if not bank:
            has_error = True
            messages.error(request,  'Client Bank is required')

        if not has_error:
            num_results = Report.objects.filter(
                upi=request.POST['upi'].upper()).count()
            if num_results > 0:
                has_error = True
                messages.error(request,  'Report with this UPI Exists')
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
                                        upi=upi.upper(),
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
        upi = request.POST['upi']
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
        if contact and len(contact) is not 10:
            has_error = True
            messages.error(
                request,  'The Contact phone should be  10 characters')

        if not upi:
            has_error = True
            messages.error(request,  'UPI is required')
        if not inspection_date:
            has_error = True
            messages.error(request,  'Inspection Date is required')
        if not delivery_date:
            has_error = True
            messages.error(request,  'Delivery Date  is required')
        if not amount:
            amount = 0
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
            report.upi = upi
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
    if report.approved == True:
        report.approved = False
        report.approved_at = datetime.datetime.now()
        report.approval_date = None
    else:
        report.approved = True
        report.approved_at = datetime.datetime.now()
        report.approval_date = datetime.date.today()
    report.save()
    messages.success(request, 'Report status updated Successfully')
    return redirect('report', id)


@login_required(login_url='/accounts/login')
def report_verified(request, id):
    report = Report.objects.get(id=id)
    if report.paid == True:
        report.paid = False
        report.verified_at = None
    else:
        report.paid = True
        report.verified_at = datetime.datetime.now()

    report.save()
    messages.success(
        request, 'Payment verification status updated Successfully')
    return redirect('reports')


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
    all_reports = Report.objects.filter(approved=True)
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

    todays_reports = Report.objects.filter(
        approved=True,  approval_date=datetime.date.today())

    for td in todays_reports:
        todays_amount += td.amount
        todays_count += 1

    start_date = datetime.datetime.today(
    ) - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)

    this_week_reports = Report.objects.filter(
        approved=True, approval_date__gte=start_date.date())

    for td in this_week_reports:
        this_week_amount += td.amount
        this_week_count += 1

    months_first_day = datetime.datetime.today().date().replace(day=1)
    this_month_reports = Report.objects.filter(
        approved=True, approval_date__gte=months_first_day)

    for td in this_month_reports:
        this_month_amount += td.amount
        this_month_count += 1

    start_date = starting_day_of_current_year = datetime.datetime.now(
    ).date().replace(month=1, day=1)
    this_year_reports = Report.objects.filter(
        approved=True, approval_date__gte=start_date)

    for one in this_year_reports:
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

        'today_reports': 'today_reports',
        'this_week_reports': 'this_week_reports',
        'this_year_reports': 'this_year_reports',
        'this_months_reports': 'this_months_reports'

    }

    return render(request, 'reports/stats.html', context)


def report_stats_rest(request):
    all_reports = Report.objects.filter(approved=True)
    today_month, today_year = datetime.datetime.today(
    ).month, datetime.datetime.today().year
    months_data = {}
    week_days_data = {}

    def get_amount_for_month(month):
        month_amount = 0
        for one in all_reports:
            month_, year = one.approved_at.month, one.approved_at.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        today_month, today_year = x, datetime.datetime.today().year
        for one in all_reports:
            months_data[x] = get_amount_for_month(x)

    def get_amount_for_day(x, today_day, month, today_year):
        day_amount = 0
        for one in all_reports:
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
        for one in all_reports:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {"months": months_data, "days": week_days_data}
    return JsonResponse({'data': data}, safe=False)

    return JsonResponse({'data': data}, safe=False)


def get_income_query_set(period):
    today = datetime.date.today()
    if period == 'today_reports':
        reports = Report.objects.filter(approval_date=today)
        return reports
    elif period == 'this_months_reports':
        months_first_day = datetime.datetime.today().date().replace(day=1)
        return Report.objects.filter(approved=True, approval_date__gte=months_first_day)

    elif period == 'this_week_reports':
        start_date = datetime.datetime.today(
        ) - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)

        reports = Report.objects.filter(
            approved=True, approval_date__gte=start_date.date())
        return reports

    elif period == 'this_year_reports':
        start_date = starting_day_of_current_year = datetime.datetime.now(
        ).date().replace(month=1, day=1)
        reports = Report.objects.filter(
            approved=True, approval_date__gte=start_date)
        return reports


def generate_pdf(queryset, request, period, total, title):
    """Generate pdf."""

    # Rendered
    html_string = render_to_string(
        'reports/pdf-output.html', {'reports': queryset,
                                    'period': period,
                                    'total': total,
                                    'title': title,
                                    'current_site': get_current_site(request).domain})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def report_export(request, period, total):

    options = {'today_reports': ' REPORTS  TODAY',
               'this_week_reports': 'REPORTS THIS WEEK',
               'this_year_reports': 'REPORTS THIS YEAR',
               'this_months_reports': 'REPORTS THIS MONTH'}

    rows = get_income_query_set(period=period)
    return generate_pdf(rows, request, period, total, options[period])
