
from django.urls import path

from .views import (
    AdminDashboardStatsAPIView,
    AdminRecentUsersAPIView,
    AdminRecentActivitiesAPIView,
)

urlpatterns = [
    path(
        "stats/",
        AdminDashboardStatsAPIView.as_view(),
        name="admin-dashboard-stats"
    ),

    path(
        "recent-users/",
        AdminRecentUsersAPIView.as_view(),
        name="admin-recent-users"
    ),

    path(
        "recent-activities/",
        AdminRecentActivitiesAPIView.as_view(),
        name="admin-recent-activities"
    ),
]
