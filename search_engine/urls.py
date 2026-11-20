
from django.urls import path

from .views import (
    GlobalSearchAPIView,
    NoteSearchAPIView,
    DocumentSearchAPIView,
    QuizSearchAPIView,
    FlashcardSearchAPIView,
    RecommendationAPIView,
)

urlpatterns = [
    path(
        "",
        GlobalSearchAPIView.as_view(),
        name="global-search"
    ),

    path(
        "notes/",
        NoteSearchAPIView.as_view(),
        name="search-notes"
    ),

    path(
        "documents/",
        DocumentSearchAPIView.as_view(),
        name="search-documents"
    ),

    path(
        "quizzes/",
        QuizSearchAPIView.as_view(),
        name="search-quizzes"
    ),

    path(
        "flashcards/",
        FlashcardSearchAPIView.as_view(),
        name="search-flashcards"
    ),

    path(
        "recommendations/",
        RecommendationAPIView.as_view(),
        name="recommendations"
    ),
]
