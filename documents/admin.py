from django.contrib import admin
from .models import StudyDocument


@admin.register(StudyDocument)
class StudyDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "user",
        "file_type",
        "status",
        "created_at",
    )

    list_filter = ("file_type", "status", "created_at")

    search_fields = ("title", "user__username")

    readonly_fields = (
        "file_size",
        "extracted_text",
        "created_at",
        "updated_at",
    )