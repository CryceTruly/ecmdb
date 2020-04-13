from django.contrib import admin
from . import models


class BankAdmin(admin.ModelAdmin):

    list_display = ('name', 'added_at')
    search_fields = ('name',)
    list_per_page = 25


admin.site.register(models.Bank, BankAdmin)
