from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_connected', 'is_42', 'avatar', 'friends', 'nickname', 'blocked_users', 'chat_invitation')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (

        (None, {'fields': ('is_connected', 'is_42', 'avatar', 'friends', 'nickname', 'blocked_users', 'chat_invitation')}),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_connected', 'is_42', 'avatar', 'nickname', 'chat_invitation')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'nickname')
    filter_horizontal = ('friends',)


admin.site.register(MyUser, CustomUserAdmin)
