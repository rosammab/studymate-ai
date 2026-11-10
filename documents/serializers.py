
from pathlib import Path
from rest_framework import serializers

from .models import StudyDocument


class StudyDocumentSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)

    class Meta:
        model = StudyDocument
        fields = [
            "id",
            "title",
            "file",
            "file_type",
            "file_size",
            "extracted_text",
            "status",
            "error_message",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "file_type",
            "file_size",
            "extracted_text",
            "status",
            "error_message",
            "created_at",
            "updated_at",
        ]

    def validate_file(self, value):
        extension = Path(value.name).suffix.lower()

        allowed_extensions = [".pdf", ".docx"]

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF and DOCX files are supported."
            )

        max_size = 10 * 1024 * 1024  # 10 MB

        if value.size > max_size:
            raise serializers.ValidationError(
                "File size cannot exceed 10 MB."
            )

        return value

    def create(self, validated_data):
        if not validated_data.get("title"):
            validated_data["title"] = Path(
                validated_data["file"].name
            ).stem

        return super().create(validated_data)
