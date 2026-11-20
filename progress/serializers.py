
from rest_framework import serializers
from .models import StudyActivity, UserProgress


class StudyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyActivity
        fields = [
            "id",
            "activity_type",
            "activity_date",
            "duration_minutes",
            "count",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_duration_minutes(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Duration cannot be negative."
            )
        return value

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Count must be at least 1."
            )
        return value


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = [
            "total_study_minutes",
            "total_quizzes",
            "total_flashcards_reviewed",
            "current_streak",
            "longest_streak",
            "updated_at",
        ]
        read_only_fields = fields
