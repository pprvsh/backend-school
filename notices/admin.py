from django.contrib import admin

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "priority_level",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
    )

    list_filter = (
        "category",
        "priority_level",
        "created_at",
    )