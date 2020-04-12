from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="reports"),
    path('add-report', views.add_report, name="add_report"),
    path('report/<int:id>', views.report, name="report"),
    path('report/edit/<int:id>', views.report_edit, name="report-edit"),
    path('search_reports', views.search_reports, name='search_reports'),
    path('report/approve/<int:id>', views.report_approve, name='report-approve'),
    path('make-reciept/<int:id>',
         views.report_reciept, name='make-reciept'),
    path('stats', views.report_stats, name="report-summary"),
    path('report-summary-rest', views.report_stats_rest,
         name='reports-summary-rest'),
    path('add_report_comments/<int:id>',
         views.add_report_comments, name='add_report_comments')
]
