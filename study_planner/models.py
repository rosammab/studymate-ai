
from django.db import models
from django.contrib.auth.models import User


class StudyPlan(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_plans"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class StudySession(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("skipped", "Skipped"),
    ]

    study_plan = models.ForeignKey(
        StudyPlan,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    scheduled_date = models.DateField()

    start_time = models.TimeField(null=True, blank=True)

    duration_minutes = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_date", "start_time"]

    def __str__(self):
        return self.title


class StudyGoal(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_goals"
    )

    title = models.CharField(max_length=255)

    target_minutes = models.PositiveIntegerField()

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class StudyReminder(models.Model):

    REMINDER_STATUS = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_reminders"
    )

    session = models.ForeignKey(
        StudySession,
        on_delete=models.CASCADE,
        related_name="reminders",
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)

    message = models.TextField(blank=True)

    reminder_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=REMINDER_STATUS,
        default="pending"
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["reminder_time"]

    def __str__(self):
        return f"{self.title} - {self.user}"