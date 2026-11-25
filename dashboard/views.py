
from django.apps import apps
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import (
    AdminDashboardStatsSerializer,
    RecentUserSerializer,
    RecentActivitySerializer,
)


def get_model_count(app_label, model_name):
    """
    Return the count of a model if it exists.
    """
    try:
        model = apps.get_model(app_label, model_name)
        return model.objects.count()
    except LookupError:
        return 0


class AdminDashboardStatsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        User = get_user_model()

        data = {
            "total_users": User.objects.count(),

            "total_notes": get_model_count(
                "notes", "Note"
            ),

            "total_flashcard_sets": get_model_count(
                "flashcards", "FlashcardSet"
            ),

            "total_flashcards": get_model_count(
                "flashcards", "Flashcard"
            ),

            "total_quizzes": get_model_count(
                "quizzes", "Quiz"
            ),

            "total_quiz_attempts": get_model_count(
                "quizzes", "QuizAttempt"
            ),

            "total_documents": get_model_count(
                "documents", "StudyDocument"
            ),

            "total_study_plans": get_model_count(
                "study_planner", "StudyPlan"
            ),

            "total_study_sessions": get_model_count(
                "study_planner", "StudySession"
            ),

            "total_notifications": get_model_count(
                "notifications", "Notification"
            ),

            "unread_notifications": 0,

            "total_study_activities": get_model_count(
                "progress", "StudyActivity"
            ),
        }

        try:
            Notification = apps.get_model(
                "notifications", "Notification"
            )

            data["unread_notifications"] = (
                Notification.objects.filter(is_read=False).count()
            )

        except LookupError:
            pass

        serializer = AdminDashboardStatsSerializer(data)

        return Response(serializer.data)


class AdminRecentUsersAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        User = get_user_model()

        users = User.objects.order_by("-date_joined")[:10]

        serializer = RecentUserSerializer(
            users,
            many=True
        )

        return Response(serializer.data)


class AdminRecentActivitiesAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            StudyActivity = apps.get_model(
                "progress", "StudyActivity"
            )

        except LookupError:
            return Response([])

        activities = StudyActivity.objects.order_by(
            "-created_at"
        )[:10]

        serializer = RecentActivitySerializer(
            activities,
            many=True
        )

        return Response(serializer.data)
