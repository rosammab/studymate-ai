
from pathlib import Path

from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import StudyDocument
from .serializers import StudyDocumentSerializer
from .utils import extract_document_text


class DocumentListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = StudyDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyDocument.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):

        uploaded_file = serializer.validated_data["file"]

        extension = Path(uploaded_file.name).suffix.lower()

        file_type = extension.lstrip(".")

        document = serializer.save(
            user=self.request.user,
            file_type=file_type,
            file_size=uploaded_file.size,
            status="processing"
        )

        try:
            extracted_text = extract_document_text(
                document.file.path,
                document.file_type
            )

            if not extracted_text:
                raise ValueError(
                    "No readable text found in the document. "
                    "Scanned PDFs may require OCR."
                )

            document.extracted_text = extracted_text
            document.status = "completed"
            document.error_message = ""

        except Exception as error:
            document.status = "failed"
            document.error_message = str(error)

        document.save()


class DocumentDetailAPIView(generics.RetrieveDestroyAPIView):

    serializer_class = StudyDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyDocument.objects.filter(
            user=self.request.user
        )

    @transaction.atomic
    def perform_destroy(self, instance):
        file = instance.file

        instance.delete()

        if file:
            file.delete(save=False)
