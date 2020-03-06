from django.contrib import admin
from .models import Expense
# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('requester', 'amount', 'requested_on', 'status', 'purpose')
    search_fields = ('requester',)
    list_per_page = 25


admin.site.register(Expense, ExpenseAdmin)
