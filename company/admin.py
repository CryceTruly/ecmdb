from django.contrib import admin
from .models import Company
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        """Ensure the admin cannot create new term Instances."""
        return True

    def has_delete_permission(self, request, obj=None):
        """Ensure the admin cannot delete the existing Term Instance."""
        return True


admin.site.register(Company, CompanyAdmin)
