
from .models import Notification


def create_user_notification(
    user,
    title,
    message,
    notification_type="system",
):
    """
    Create a notification for a specific user.
    """

    if not user or not user.is_authenticated:
        raise ValueError("A valid authenticated user is required.")

    if not title or not title.strip():
        raise ValueError("Notification title cannot be empty.")

    if not message or not message.strip():
        raise ValueError("Notification message cannot be empty.")

    valid_types = {
        choice[0]
        for choice in Notification.NOTIFICATION_TYPES
    }

    if notification_type not in valid_types:
        raise ValueError("Invalid notification type.")

    return Notification.objects.create(
        user=user,
        title=title.strip(),
        message=message.strip(),
        notification_type=notification_type,
    )
