from django.contrib import admin
from .models import User, Profile

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'phone_number', 'is_staff', 'is_superuser')
    search_fields = ('email', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('OTP Info', {'fields': ('otp', 'otp_created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)


admin.site.register(Profile)
