
from django.db import models
from django.contrib.auth.models import User


class StudyActivity(models.Model):

    ACTIVITY_CHOICES = [
        ("quiz", "Quiz"),
        ("flashcard", "Flashcard"),
        ("study_session", "Study Session"),
        ("note", "Note"),
        ("document", "Document"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_activities"
    )

    activity_type = models.CharField(
        max_length=30,
        choices=ACTIVITY_CHOICES
    )

    activity_date = models.DateField()

    duration_minutes = models.PositiveIntegerField(default=0)

    count = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-activity_date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "activity_date"]),
            models.Index(fields=["user", "activity_type"]),
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.activity_type} - {self.activity_date}"
        )


class UserProgress(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="learning_progress"
    )

    total_study_minutes = models.PositiveIntegerField(default=0)

    total_quizzes = models.PositiveIntegerField(default=0)

    total_flashcards_reviewed = models.PositiveIntegerField(default=0)

    current_streak = models.PositiveIntegerField(default=0)

    longest_streak = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress - {self.user.username}"
