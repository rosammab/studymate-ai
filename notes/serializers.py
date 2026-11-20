
from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Note title cannot be empty."
            )
        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Note content cannot be empty."
            )
        return value.strip()
