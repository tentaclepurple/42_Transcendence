from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_connected', 'is_42', 'avatar', 'friends')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (

        (None, {'fields': ('is_connected', 'is_42', 'avatar', 'friends')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_connected', 'is_42', 'avatar')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('friends',)


admin.site.register(MyUser, CustomUserAdmin)
