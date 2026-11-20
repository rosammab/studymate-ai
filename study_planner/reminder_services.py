
from django.db import transaction
from django.utils import timezone

from .models import StudyReminder
from notifications.services import create_user_notification


def process_due_reminders():

    due_reminders = StudyReminder.objects.filter(
        status="pending",
        reminder_time__lte=timezone.now()
    ).order_by("reminder_time")

    processed_count = 0

    for reminder in due_reminders:

        with transaction.atomic():

            locked_reminder = (
                StudyReminder.objects
                .select_for_update()
                .filter(
                    id=reminder.id,
                    status="pending"
                )
                .first()
            )

            if locked_reminder is None:
                continue

            create_user_notification(
                user=locked_reminder.user,
                title=locked_reminder.title,
                message=(
                    locked_reminder.message
                    or "Your scheduled study reminder is due."
                ),
                notification_type="reminder"
            )

            locked_reminder.status = "sent"
            locked_reminder.sent_at = timezone.now()

            locked_reminder.save(
                update_fields=[
                    "status",
                    "sent_at",
                    "updated_at"
                ]
            )

            processed_count += 1

    return processed_count
