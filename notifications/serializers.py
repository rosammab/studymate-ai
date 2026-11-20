
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "message",
            "notification_type",
            "is_read",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "is_read",
            "created_at",
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Notification title cannot be empty."
            )
        return value

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Notification message cannot be empty."
            )
        return value
