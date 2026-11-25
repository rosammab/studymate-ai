
from django.urls import path

from .views import (
    NotificationListAPIView,
    NotificationDetailAPIView,
    MarkNotificationReadAPIView,
    MarkAllNotificationsReadAPIView,
    UnreadNotificationCountAPIView,
)

urlpatterns = [
    path(
        "",
        NotificationListAPIView.as_view(),
        name="notification-list",
    ),
    path(
        "<int:pk>/",
        NotificationDetailAPIView.as_view(),
        name="notification-detail",
    ),
    path(
        "<int:pk>/read/",
        MarkNotificationReadAPIView.as_view(),
        name="notification-mark-read",
    ),
    path(
        "mark-all-read/",
        MarkAllNotificationsReadAPIView.as_view(),
        name="notification-mark-all-read",
    ),
    path(
        "unread-count/",
        UnreadNotificationCountAPIView.as_view(),
        name="notification-unread-count",
    ),
]
