from django.contrib import admin
from .models import StudyPlan, StudySession, StudyGoal


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "user",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = ("status", "start_date")

    search_fields = ("title", "user__username")


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "study_plan",
        "scheduled_date",
        "duration_minutes",
        "status",
    )

    list_filter = ("status", "scheduled_date")

    search_fields = ("title",)


@admin.register(StudyGoal)
class StudyGoalAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "user",
        "target_minutes",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = ("status",)

    search_fields = ("title", "user__username")