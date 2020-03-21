from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="reports"),
    path('add-report', views.add_report, name="add_report"),
    path('report/<int:id>', views.report, name="report"),
    path('report/edit/<int:id>', views.report_edit, name="report-edit"),
    path('reports/search_reports', views.search_reports, name='search_reports'),
    path('report/approve/<int:id>', views.report_approve, name='report-approve')
]
