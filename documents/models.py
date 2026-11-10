
from django.db import models
from django.contrib.auth.models import User


class StudyDocument(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    FILE_TYPE_CHOICES = [
        ("pdf", "PDF"),
        ("docx", "DOCX"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_documents"
    )

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to="study_documents/%Y/%m/"
    )

    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPE_CHOICES
    )

    file_size = models.PositiveBigIntegerField(default=0)

    extracted_text = models.TextField(
        blank=True,
        default=""
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
