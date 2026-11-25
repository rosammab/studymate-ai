
from rest_framework import serializers

from .models import Conversation, ChatMessage


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Conversation title cannot be empty."
            )

        return value


class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "role",
            "content",
            "created_at",
        ]
        read_only_fields = fields


class SendMessageSerializer(serializers.Serializer):

    content = serializers.CharField(
        max_length=10000,
        allow_blank=False,
        trim_whitespace=True
    )

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Message cannot be empty."
            )

        return value
