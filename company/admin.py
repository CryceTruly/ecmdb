from django.contrib import admin
from .models import Company
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        """Ensure the admin cannot create new Company Instances."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Ensure the admin cannot delete the existing Company Instance."""
        return False


admin.site.register(Company, CompanyAdmin)
