
from django.db import transaction
from django.shortcuts import get_object_or_404
from .artifact_services import generate_pdf, generate_image
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, ChatMessage
from .serializers import (
    ConversationSerializer,
    ChatMessageSerializer,
    SendMessageSerializer,
)
from .services import (
    generate_ai_response,
    AIServiceError,
)


class ConversationListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConversationDetailAPIView(generics.RetrieveDestroyAPIView):

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            user=self.request.user
        )


class ConversationMessageListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_conversation(self, request, pk):
        return get_object_or_404(
            Conversation,
            pk=pk,
            user=request.user
        )

    def get(self, request, pk):
        conversation = self.get_conversation(request, pk)

        messages = conversation.messages.all()

        serializer = ChatMessageSerializer(
            messages,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, pk):
        conversation = self.get_conversation(request, pk)

        input_serializer = SendMessageSerializer(
            data=request.data
        )

        input_serializer.is_valid(raise_exception=True)

        user_content = input_serializer.validated_data["content"]

        # Get the latest 20 previous messages for context.
        previous_messages = list(
            conversation.messages.order_by(
                "-created_at"
            )[:20]
        )

        previous_messages.reverse()

        ai_messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in previous_messages
        ]

        ai_messages.append({
            "role": "user",
            "content": user_content,
        })

        # Generate the response before saving the new messages.
        try:
            assistant_content = generate_ai_response(ai_messages)

        except AIServiceError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Save both messages together.
        with transaction.atomic():

            user_message = ChatMessage.objects.create(
                conversation=conversation,
                role="user",
                content=user_content
            )

            assistant_message = ChatMessage.objects.create(
                conversation=conversation,
                role="assistant",
                content=assistant_content
            )

            # Automatically use the first message as the title.
            if conversation.title == "New conversation":
                conversation.title = user_content[:200]

            conversation.save()

        return Response(
            {
                "conversation_id": conversation.id,
                "user_message": ChatMessageSerializer(
                    user_message
                ).data,
                "assistant_message": ChatMessageSerializer(
                    assistant_message
                ).data,
            },
            status=status.HTTP_201_CREATED
        )

class GeneratePDFAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get("prompt", "").strip()

        if not prompt:
            return Response(
                {"error": "Please provide a PDF topic."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(prompt) > 2000:
            return Response(
                {"error": "The prompt is too long."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            artifact = generate_pdf(request.user, prompt)

        except AIServiceError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            {
                "message": "PDF generated successfully.",
                "id": artifact.id,
                "title": artifact.title,
                "file_url": request.build_absolute_uri(
                    artifact.file.url
                ),
                "created_at": artifact.created_at,
            },
            status=status.HTTP_201_CREATED
        )


class GenerateImageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get("prompt", "").strip()

        if not prompt:
            return Response(
                {"error": "Please describe the image."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(prompt) > 2000:
            return Response(
                {"error": "The prompt is too long."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            artifact = generate_image(request.user, prompt)

        except AIServiceError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            {
                "message": "Image generated successfully.",
                "id": artifact.id,
                "title": artifact.title,
                "file_url": request.build_absolute_uri(
                    artifact.file.url
                ),
                "created_at": artifact.created_at,
            },
            status=status.HTTP_201_CREATED
        )

