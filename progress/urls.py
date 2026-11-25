
from django.urls import path

from .views import (
    StudyActivityListAPIView,
    StudyActivityDetailAPIView,
    UserProgressAPIView,
    DailyProgressAPIView,
    ActivityBreakdownAPIView,
)

app_name = "progress"

urlpatterns = [

    # Study Activities
    path(
        "activities/",
        StudyActivityListAPIView.as_view(),
        name="activity-list"
    ),

    path(
        "activities/<int:pk>/",
        StudyActivityDetailAPIView.as_view(),
        name="activity-detail"
    ),

    # User Progress
    path(
        "summary/",
        UserProgressAPIView.as_view(),
        name="progress-summary"
    ),

    # Daily Progress
    path(
        "daily/",
        DailyProgressAPIView.as_view(),
        name="daily-progress"
    ),

    # Activity Breakdown
    path(
        "breakdown/",
        ActivityBreakdownAPIView.as_view(),
        name="activity-breakdown"
    ),
]