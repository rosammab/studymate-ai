from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    university = models.CharField(
        max_length=100
    )

    course = models.CharField(
        max_length=100
    )

    year_of_study = models.PositiveIntegerField()

    state = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    board = models.CharField(
        max_length=50,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    study_goal = models.CharField(
        max_length=255,
        blank=True
    )

    preferred_language = models.CharField(
        max_length=50,
        default="English"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username
