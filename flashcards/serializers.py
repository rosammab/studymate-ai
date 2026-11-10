
from rest_framework import serializers
from .models import FlashcardReview, FlashcardSet, Flashcard


class FlashcardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flashcard
        fields = [
            "id",
            "question",
            "answer",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_question(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Question cannot be empty."
            )
        return value.strip()

    def validate_answer(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Answer cannot be empty."
            )
        return value.strip()


class FlashcardSetSerializer(serializers.ModelSerializer):

    cards = FlashcardSerializer(many=True, read_only=True)

    class Meta:
        model = FlashcardSet
        fields = [
            "id",
            "title",
            "description",
            "cards",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "cards",
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Flashcard set title cannot be empty."
            )
        return value.strip()
class FlashcardReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlashcardReview
        fields = [
            "id",
            "flashcard",
            "result",
            "reviewed_at",
        ]

        read_only_fields = [
            "id",
            "reviewed_at",
        ]

    def validate_result(self, value):
        if value not in ["known", "missed"]:
            raise serializers.ValidationError(
                "Result must be either 'known' or 'missed'."
            )

        return value