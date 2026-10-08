from django.contrib import admin

from .models import AdmissionInquiry


@admin.register(AdmissionInquiry)
class AdmissionInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "parent_name",
        "email",
        "phone",
        "student_grade",
        "status",
    )

    search_fields = (
        "parent_name",
        "email",
        "phone",
    )

    list_filter = (
        "status",
        "student_grade",
    )