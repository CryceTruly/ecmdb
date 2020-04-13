from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'owner', 'location',
                    'contact', 'client', 'plot_no', 'inspection_date', 'approved', 'paid', 'verified_at')
    search_fields = ('owner', 'location',
                     'contact', 'client', 'plot_no', 'inspection_date', 'approved', 'paid', 'verified_at')
    list_per_page = 25


admin.site.register(Report, ReportAdmin)
