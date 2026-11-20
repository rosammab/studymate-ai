
from django.urls import path

from .views import (
    NotificationListCreateAPIView,
    NotificationDetailAPIView,
    MarkNotificationReadAPIView,
    MarkAllNotificationsReadAPIView,
    UnreadNotificationCountAPIView,
)

urlpatterns = [
    path(
        "",
        NotificationListCreateAPIView.as_view(),
        name="notification-list-create"
    ),

    path(
        "<int:pk>/",
        NotificationDetailAPIView.as_view(),
        name="notification-detail"
    ),

    path(
        "<int:pk>/read/",
        MarkNotificationReadAPIView.as_view(),
        name="notification-mark-read"
    ),

    path(
        "mark-all-read/",
        MarkAllNotificationsReadAPIView.as_view(),
        name="notification-mark-all-read"
    ),

    path(
        "unread-count/",
        UnreadNotificationCountAPIView.as_view(),
        name="notification-unread-count"
    ),
]
