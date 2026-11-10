
from django.db import models
from django.contrib.auth.models import User


class FlashcardSet(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="flashcard_sets"
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Flashcard(models.Model):
    flashcard_set = models.ForeignKey(
        FlashcardSet,
        on_delete=models.CASCADE,
        related_name="cards"
    )

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:50]
class FlashcardReview(models.Model):

    REVIEW_CHOICES = [
        ("known", "Known"),
        ("missed", "Missed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="flashcard_reviews"
    )

    flashcard = models.ForeignKey(
        Flashcard,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    result = models.CharField(
        max_length=10,
        choices=REVIEW_CHOICES
    )

    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.flashcard.id} - {self.result}"