from django.contrib import admin
from .models import StudyActivity, UserProgress


@admin.register(StudyActivity)
class StudyActivityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "activity_type",
        "activity_date",
        "duration_minutes",
        "count",
    )

    list_filter = ("activity_type", "activity_date")

    search_fields = ("user__username",)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "total_study_minutes",
        "total_quizzes",
        "total_flashcards_reviewed",
        "current_streak",
        "longest_streak",
    )

    search_fields = ("user__username",)

    readonly_fields = ("updated_at",)