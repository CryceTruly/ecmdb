from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'email', 'role', 'is_active')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name',)
    list_per_page = 25


admin.site.register(User, UserAdmin)
