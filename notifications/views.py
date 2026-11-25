
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(
            user=self.request.user
        )

        unread = self.request.query_params.get("unread")

        if unread == "true":
            queryset = queryset.filter(is_read=False)
        elif unread == "false":
            queryset = queryset.filter(is_read=True)

        notification_type = self.request.query_params.get("type")

        if notification_type:
            valid_types = {
                choice[0]
                for choice in Notification.NOTIFICATION_TYPES
            }

            if notification_type not in valid_types:
                return Notification.objects.none()

            queryset = queryset.filter(
                notification_type=notification_type
            )

        return queryset


class NotificationDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )


class MarkNotificationReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(
                pk=pk,
                user=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {"message": "Notification not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            {
                "message": "Notification marked as read.",
                "notification": NotificationSerializer(
                    notification
                ).data
            },
            status=status.HTTP_200_OK
        )


class MarkAllNotificationsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)

        return Response(
            {
                "message": "All notifications marked as read.",
                "updated_count": updated_count
            },
            status=status.HTTP_200_OK
        )


class UnreadNotificationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        return Response(
            {"unread_count": unread_count},
            status=status.HTTP_200_OK
        )
