
from django.urls import path

from .views import (
    ConversationListCreateAPIView,
    ConversationDetailAPIView,
    ConversationMessageListCreateAPIView,
    GeneratePDFAPIView,
    GenerateImageAPIView,
)

urlpatterns = [
    path(
        "conversations/",
        ConversationListCreateAPIView.as_view(),
        name="conversation-list-create"
    ),

    path(
        "conversations/<int:pk>/",
        ConversationDetailAPIView.as_view(),
        name="conversation-detail"
    ),

    path(
        "conversations/<int:pk>/messages/",
        ConversationMessageListCreateAPIView.as_view(),
        name="conversation-messages"
    ),

    path(
        "generate-pdf/",
        GeneratePDFAPIView.as_view(),
        name="generate-pdf"
    ),

    path(
        "generate-image/",
        GenerateImageAPIView.as_view(),
        name="generate-image"
    ),
]
