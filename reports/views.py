from django.shortcuts import render, redirect, get_object_or_404
from banks.models import Bank
from django.contrib import messages
from .models import Report
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def index(request):
    context = {
        'my_reports': Report.objects.filter(created_by=request.user)
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
        contact = request.POST['owner_contact']
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
            try:
                get_object_or_404(plot_no=request.POST['plot_no'])

                has_error = True
                messages.error(request,  'Plot Number Exists')
                return render(request, 'reports/add_report.html', context)
            except Exception as identifier:
                pass
        if not has_error:
            rep = Report.objects.create(created_by=request.user,
                                        owner=owner,
                                        location=location,
                                        amount_charged=amount,
                                        client=bank,
                                        purpose=purpose,
                                        contact=contact,
                                        plot_no=plot_no,
                                        inspection_date=inspection_date,
                                        delivery_date=delivery_date,
                                        report_payed_for=True,
                                        reason_for_not_paying='N/A')

            if rep:
                messages.success(request, 'Report Submitted Successfully')
                return redirect('reports')

        return render(request, 'reports/add_report.html', context)
