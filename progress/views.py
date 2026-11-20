
from datetime import timedelta

from django.db.models import Sum, Count
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StudyActivity
from .serializers import (
    StudyActivitySerializer,
    UserProgressSerializer,
)
from .services import update_user_progress


class StudyActivityListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StudyActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StudyActivity.objects.filter(user=self.request.user)

        activity_type = self.request.query_params.get("type")

        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        update_user_progress(self.request.user)


class StudyActivityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudyActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudyActivity.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        update_user_progress(self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
        update_user_progress(self.request.user)


class UserProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = update_user_progress(request.user)

        serializer = UserProgressSerializer(progress)

        return Response(serializer.data)


class DailyProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            days = int(request.query_params.get("days", 7))
        except (TypeError, ValueError):
            return Response(
                {"error": "Days must be a valid integer."},
                status=400
            )

        if days < 1 or days > 90:
            return Response(
                {"error": "Days must be between 1 and 90."},
                status=400
            )

        today = timezone.localdate()
        start_date = today - timedelta(days=days - 1)

        activities = (
            StudyActivity.objects.filter(
                user=request.user,
                activity_date__range=[start_date, today]
            )
            .values("activity_date")
            .annotate(
                total_minutes=Sum("duration_minutes"),
                activity_count=Count("id"),
                total_count=Sum("count")
            )
            .order_by("activity_date")
        )

        return Response({
            "days": days,
            "start_date": start_date,
            "end_date": today,
            "activities": activities
        })


class ActivityBreakdownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        breakdown = (
            StudyActivity.objects.filter(user=request.user)
            .values("activity_type")
            .annotate(
                total_minutes=Sum("duration_minutes"),
                total_count=Sum("count"),
                records=Count("id")
            )
            .order_by("activity_type")
        )

        return Response(breakdown)
