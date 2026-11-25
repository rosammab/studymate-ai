
from django.contrib import admin

from .models import Conversation, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ["role", "content", "created_at"]
    can_delete = False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "user__username",
        "user__email",
    ]

    list_filter = ["created_at"]

    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "conversation",
        "role",
        "created_at",
    ]

    list_filter = ["role", "created_at"]

    search_fields = ["content"]
