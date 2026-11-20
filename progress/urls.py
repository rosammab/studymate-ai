
from django.urls import path

from .views import (
    StudyActivityListCreateAPIView,
    StudyActivityDetailAPIView,
    UserProgressAPIView,
    DailyProgressAPIView,
    ActivityBreakdownAPIView,
)

urlpatterns = [
    path(
        "activities/",
        StudyActivityListCreateAPIView.as_view(),
        name="activity-list-create"
    ),
    path(
        "activities/<int:pk>/",
        StudyActivityDetailAPIView.as_view(),
        name="activity-detail"
    ),
    path(
        "summary/",
        UserProgressAPIView.as_view(),
        name="progress-summary"
    ),
    path(
        "daily/",
        DailyProgressAPIView.as_view(),
        name="daily-progress"
    ),
    path(
        "breakdown/",
        ActivityBreakdownAPIView.as_view(),
        name="activity-breakdown"
    ),
]
