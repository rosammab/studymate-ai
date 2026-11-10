from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone_number",
        "university",
        "course",
        "country",
    )

    search_fields = (
        "user__username",
        "phone_number",
        "university",
    )

    list_filter = (
        "country",
        "course",
    )