
from .models import Notification


def create_user_notification(
    user,
    title,
    message,
    notification_type="system"
):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )
