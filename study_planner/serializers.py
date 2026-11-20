
from rest_framework import serializers
from .models import StudyPlan, StudySession, StudyGoal,StudyReminder


class StudySessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudySession
        fields = [
            "id",
            "study_plan",
            "title",
            "description",
            "scheduled_date",
            "start_time",
            "duration_minutes",
            "status",
            "completed_at",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "completed_at",
            "created_at",
        ]

    def validate_duration_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Duration must be greater than zero."
            )
        return value

    def validate_study_plan(self, value):
        request = self.context.get("request")

        if request and value.user != request.user:
            raise serializers.ValidationError(
                "You cannot add sessions to another user's study plan."
            )

        return value

    def validate(self, attrs):
        plan = attrs.get(
            "study_plan",
            getattr(self.instance, "study_plan", None)
        )

        scheduled_date = attrs.get(
            "scheduled_date",
            getattr(self.instance, "scheduled_date", None)
        )

        if plan and scheduled_date:
            if not plan.start_date <= scheduled_date <= plan.end_date:
                raise serializers.ValidationError({
                    "scheduled_date":
                    "Session date must be within the study plan dates."
                })

        return attrs


class StudyPlanSerializer(serializers.ModelSerializer):

    sessions = StudySessionSerializer(many=True, read_only=True)

    session_count = serializers.IntegerField(
        source="sessions.count",
        read_only=True
    )

    class Meta:
        model = StudyPlan
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "status",
            "session_count",
            "sessions",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "session_count",
            "sessions",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None)
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "End date cannot be before start date."
            })

        return attrs


class StudyGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyGoal
        fields = [
            "id",
            "title",
            "target_minutes",
            "start_date",
            "end_date",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]

    def validate_target_minutes(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Target minutes must be greater than zero."
            )
        return value

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        end_date = attrs.get(
            "end_date",
            getattr(self.instance, "end_date", None)
        )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "end_date": "End date cannot be before start date."
            })

        return attrs




class StudyReminderSerializer(serializers.ModelSerializer):

    session_title = serializers.CharField(
        source="session.title",
        read_only=True
    )

    class Meta:
        model = StudyReminder

        fields = [
            "id",
            "user",
            "session",
            "session_title",
            "title",
            "message",
            "reminder_time",
            "status",
            "sent_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "status",
            "sent_at",
            "created_at",
            "updated_at",
        ]

    def validate_session(self, session):
        request = self.context.get("request")

        if session and request:
            if session.study_plan.user_id != request.user.id:
                raise serializers.ValidationError(
                    "You cannot create a reminder for another user's session."
                )

        return session

    def validate_reminder_time(self, value):
        from django.utils import timezone

        if value <= timezone.now():
            raise serializers.ValidationError(
                "Reminder time must be in the future."
            )

        return value
