from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Doctor, Patient, PatientDoctorMapping, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "name", "is_staff", "is_active")
    fieldsets = ((None, {"fields": ("email", "password")}), ("Personal info", {"fields": ("name", "first_name", "last_name")}), ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}), ("Important dates", {"fields": ("last_login", "date_joined")}))
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "name", "password1", "password2", "is_staff", "is_superuser")} ),)
    username = None
    search_fields = ("email", "name")


admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(PatientDoctorMapping)
