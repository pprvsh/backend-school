from django.contrib import admin

from .models import Department, Faculty


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "department",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "email",
    )
    list_filter = (
        "department",
        "is_active",
    )