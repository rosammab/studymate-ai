
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from progress.services import create_study_activity
from notifications.services import create_user_notification

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import StudyPlan, StudySession, StudyGoal,StudyReminder
from .serializers import (
    StudyPlanSerializer,
    StudySessionSerializer,
    StudyGoalSerializer,
    StudyReminderSerializer
    
)


class StudyPlanListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = StudyPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyPlan.objects.filter(
            user=self.request.user
        ).prefetch_related("sessions")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudyPlanDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = StudyPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyPlan.objects.filter(
            user=self.request.user
        ).prefetch_related("sessions")


class StudySessionListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = StudySessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudySession.objects.filter(
            study_plan__user=self.request.user
        ).select_related("study_plan")

    def perform_create(self, serializer):
        study_plan = serializer.validated_data["study_plan"]

        if study_plan.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You cannot create a session for this study plan."
            )

        serializer.save()


class StudySessionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = StudySessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudySession.objects.filter(
            study_plan__user=self.request.user
        )




class StudySessionCompleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        session = get_object_or_404(
            StudySession,
            pk=pk,
            study_plan__user=request.user
        )

        # Prevent duplicate completion
        if session.status == "completed":
            return Response(
                {
                    "message": "Session is already completed.",
                    "progress_updated": False,
                    "notification_created": False
                },
                status=status.HTTP_200_OK
            )

        with transaction.atomic():

            session.status = "completed"
            session.completed_at = timezone.now()

            session.save(
                update_fields=["status", "completed_at"]
            )

            # Automatically update progress
            create_study_activity(
                user=request.user,
                activity_type="study_session",
                duration_minutes=session.duration_minutes,
                count=1,
                activity_date=timezone.localdate()
            )

            # Automatically create notification
            create_user_notification(
                user=request.user,
                title="Study Session Completed",
                message=(
                    f"You completed your study session: "
                    f"{session.title}."
                ),
                notification_type="study"
            )

        return Response(
            {
                "message": "Study session completed successfully.",
                "session": StudySessionSerializer(session).data,
                "progress_updated": True,
                "notification_created": True
            },
            status=status.HTTP_200_OK
        )


class StudyGoalListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = StudyGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyGoal.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudyGoalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = StudyGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyGoal.objects.filter(
            user=self.request.user
        )


class StudyPlannerSummaryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        plans = StudyPlan.objects.filter(user=user)

        sessions = StudySession.objects.filter(
            study_plan__user=user
        )

        goals = StudyGoal.objects.filter(user=user)

        total_sessions = sessions.count()

        completed_sessions = sessions.filter(
            status="completed"
        ).count()

        total_study_minutes = sessions.filter(
            status="completed"
        ).aggregate(
            total=Sum("duration_minutes")
        )["total"] or 0

        return Response({
            "total_plans": plans.count(),
            "active_plans": plans.filter(status="active").count(),
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "pending_sessions": sessions.filter(
                status="pending"
            ).count(),
            "total_study_minutes": total_study_minutes,
            "total_goals": goals.count(),
            "active_goals": goals.filter(status="active").count(),
        })
    

class StudyGoalCompleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        goal = get_object_or_404(
            StudyGoal,
            pk=pk,
            user=request.user
        )

        # Prevent duplicate notifications
        if goal.status == "completed":
            return Response(
                {
                    "message": "Study goal is already completed.",
                    "notification_created": False
                },
                status=status.HTTP_200_OK
            )

        with transaction.atomic():

            goal.status = "completed"

            goal.save(
                update_fields=["status"]
            )

            # Automatically create notification
            create_user_notification(
                user=request.user,
                title="Study Goal Achieved",
                message=(
                    f"You completed your study goal: "
                    f"{goal.title}."
                ),
                notification_type="study"
            )

        return Response(
            {
                "message": "Study goal completed successfully.",
                "goal": StudyGoalSerializer(goal).data,
                "notification_created": True
            },
            status=status.HTTP_200_OK
        )


class StudyReminderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StudyReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyReminder.objects.filter(
            user=self.request.user
        ).select_related("session", "session__study_plan")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudyReminderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyReminder.objects.filter(
            user=self.request.user
        ).select_related("session", "session__study_plan")
