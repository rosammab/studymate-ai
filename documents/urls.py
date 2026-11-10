
from django.urls import path

from .views import (
    DocumentListCreateAPIView,
    DocumentDetailAPIView,
)

app_name = "documents"

urlpatterns = [
    path(
        "",
        DocumentListCreateAPIView.as_view(),
        name="document-list-create"
    ),

    path(
        "<int:pk>/",
        DocumentDetailAPIView.as_view(),
        name="document-detail"
    ),
]
