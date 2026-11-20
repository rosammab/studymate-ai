
from django.core.management.base import BaseCommand

from study_planner.reminder_services import process_due_reminders


class Command(BaseCommand):

    help = "Process due study reminders"

    def handle(self, *args, **options):

        count = process_due_reminders()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed {count} reminder(s)."
            )
        )
