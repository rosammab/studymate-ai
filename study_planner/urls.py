
from django.urls import path
from . import views

from .views import (
    StudyPlanListCreateAPIView,
    StudyPlanDetailAPIView,
    StudySessionListCreateAPIView,
    StudySessionDetailAPIView,
    StudySessionCompleteAPIView,
    StudyGoalListCreateAPIView,
    StudyGoalDetailAPIView,
    StudyPlannerSummaryAPIView,
    StudyGoalCompleteAPIView,
    StudyReminderListCreateAPIView,
    StudyReminderDetailAPIView,
)

app_name = "study_planner"

urlpatterns = [

    # Study Plans
    path(
        "plans/",
        StudyPlanListCreateAPIView.as_view(),
        name="plan-list-create"
    ),

    path(
        "plans/<int:pk>/",
        StudyPlanDetailAPIView.as_view(),
        name="plan-detail"
    ),

    # Study Sessions
    path(
        "sessions/",
        StudySessionListCreateAPIView.as_view(),
        name="session-list-create"
    ),

    path(
        "sessions/<int:pk>/",
        StudySessionDetailAPIView.as_view(),
        name="session-detail"
    ),

    path(
        "sessions/<int:pk>/complete/",
        StudySessionCompleteAPIView.as_view(),
        name="session-complete"
    ),

    # Study Goals
    path(
        "goals/",
        StudyGoalListCreateAPIView.as_view(),
        name="goal-list-create"
    ),

    path(
        "goals/<int:pk>/",
        StudyGoalDetailAPIView.as_view(),
        name="goal-detail"
    ),

    # Dashboard Summary
    path(
        "summary/",
        StudyPlannerSummaryAPIView.as_view(),
        name="planner-summary"
    ),

    path("goals/<int:pk>/complete/",StudyGoalCompleteAPIView.as_view(),
    name="goal-complete"
),
    path(
        "reminders/",
        views.StudyReminderListCreateAPIView.as_view(),
        name="reminder-list-create"
    ),

    path(
        "reminders/<int:pk>/",
        views.StudyReminderDetailAPIView.as_view(),
        name="reminder-detail"
    ),
]
