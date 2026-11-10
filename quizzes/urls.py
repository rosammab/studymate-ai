from django.urls import path
from . import views

app_name = "quizzes"

urlpatterns = [

    # Quiz CRUD
    path(
        "",
        views.QuizListCreateAPIView.as_view(),
        name="quiz-list-create"
    ),

    path(
        "<int:pk>/",
        views.QuizDetailAPIView.as_view(),
        name="quiz-detail"
    ),

    # Questions
    path(
        "<int:quiz_id>/questions/",
        views.QuestionListAPIView.as_view(),
        name="question-list"
    ),

    path(
        "<int:quiz_id>/questions/create/",
        views.QuestionCreateAPIView.as_view(),
        name="question-create"
    ),

    # Options
    path(
        "questions/<int:question_id>/options/create/",
        views.QuizOptionCreateAPIView.as_view(),
        name="option-create"
    ),

    # Submit quiz
    path(
        "<int:quiz_id>/submit/",
        views.QuizSubmitAPIView.as_view(),
        name="quiz-submit"
    ),

    # Quiz attempts
    path(
        "attempts/",
        views.QuizAttemptListAPIView.as_view(),
        name="attempt-list"
    ),

    path(
        "attempts/<int:pk>/",
        views.QuizAttemptDetailAPIView.as_view(),
        name="attempt-detail"
    ),
]