
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import FlashcardSet, Flashcard
from .models import FlashcardReview
from .serializers import FlashcardReviewSerializer
from .serializers import (
    FlashcardSetSerializer,
    FlashcardSerializer,
)


class FlashcardSetListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List the logged-in user's flashcard sets.
    POST: Create a new flashcard set.
    """

    serializer_class = FlashcardSetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FlashcardSet.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlashcardSetDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    GET: Retrieve one flashcard set.
    PUT: Replace the set's editable data.
    PATCH: Partially update the set.
    DELETE: Delete the set.
    """

    serializer_class = FlashcardSetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FlashcardSet.objects.filter(
            user=self.request.user
        )


class FlashcardListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List cards belonging to a set.
    POST: Add a card to a set.
    """

    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Flashcard.objects.filter(
            flashcard_set__user=self.request.user,
            flashcard_set_id=self.kwargs["set_pk"]
        ).order_by("-created_at")

    def perform_create(self, serializer):
        flashcard_set = get_object_or_404(
            FlashcardSet,
            pk=self.kwargs["set_pk"],
            user=self.request.user
        )

        serializer.save(flashcard_set=flashcard_set)


class FlashcardDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    GET: Retrieve one card.
    PUT: Replace the card's editable data.
    PATCH: Partially update the card.
    DELETE: Delete the card.
    """

    serializer_class = FlashcardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Flashcard.objects.filter(
            flashcard_set__user=self.request.user
        )
class FlashcardReviewCreateAPIView(generics.CreateAPIView):

    serializer_class = FlashcardReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        flashcard_id = self.request.data.get("flashcard")

        flashcard = get_object_or_404(
            Flashcard,
            id=flashcard_id,
            flashcard_set__user=self.request.user
        )

        serializer.save(
            user=self.request.user,
            flashcard=flashcard
        )


class FlashcardReviewListAPIView(generics.ListAPIView):

    serializer_class = FlashcardReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return FlashcardReview.objects.filter(
            user=self.request.user
        ).select_related(
            "flashcard"
        ).order_by("-reviewed_at")