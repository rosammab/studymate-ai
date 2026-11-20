
from rest_framework import serializers


class AdminDashboardStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_notes = serializers.IntegerField()
    total_flashcard_sets = serializers.IntegerField()
    total_flashcards = serializers.IntegerField()
    total_quizzes = serializers.IntegerField()
    total_quiz_attempts = serializers.IntegerField()
    total_documents = serializers.IntegerField()
    total_study_plans = serializers.IntegerField()
    total_study_sessions = serializers.IntegerField()
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    total_study_activities = serializers.IntegerField()


class RecentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()


class RecentActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    activity_type = serializers.CharField()
    activity_date = serializers.DateField()
    duration_minutes = serializers.IntegerField()
    count = serializers.IntegerField()
