
from django.urls import path

from .views import (
    FlashcardSetListCreateAPIView,
    FlashcardSetDetailAPIView,
    FlashcardListCreateAPIView,
    FlashcardDetailAPIView,
    FlashcardReviewCreateAPIView,
    FlashcardReviewListAPIView,
)

app_name = "flashcards"

urlpatterns = [
    # Flashcard sets
    path(
        "sets/",
        FlashcardSetListCreateAPIView.as_view(),
        name="set-list-create"
    ),

    path(
        "sets/<int:pk>/",
        FlashcardSetDetailAPIView.as_view(),
        name="set-detail"
    ),

    # Cards inside a set
    path(
        "sets/<int:set_pk>/cards/",
        FlashcardListCreateAPIView.as_view(),
        name="card-list-create"
    ),

    # Individual card
    path(
        "cards/<int:pk>/",
        FlashcardDetailAPIView.as_view(),
        name="card-detail"
    ),
    path(
    "reviews/",
    FlashcardReviewListAPIView.as_view(),
    name="review-list"
),

path(
    "reviews/create/",
    FlashcardReviewCreateAPIView.as_view(),
    name="review-create"
),
]
