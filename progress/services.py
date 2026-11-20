
from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum, Q

from .models import StudyActivity, UserProgress


def create_study_activity(
    user,
    activity_type,
    duration_minutes=0,
    count=1,
    activity_date=None
):
    activity = StudyActivity.objects.create(
        user=user,
        activity_type=activity_type,
        activity_date=activity_date or timezone.localdate(),
        duration_minutes=duration_minutes,
        count=count
    )

    update_user_progress(user)

    return activity


def calculate_study_streak(user):
    activity_dates = set(
        StudyActivity.objects.filter(user=user)
        .values_list("activity_date", flat=True)
    )

    if not activity_dates:
        return 0, 0

    today = timezone.localdate()

    current_streak = 0
    check_date = today

    if check_date not in activity_dates:
        check_date = today - timedelta(days=1)

    while check_date in activity_dates:
        current_streak += 1
        check_date -= timedelta(days=1)

    longest_streak = 0
    streak = 0
    previous_date = None

    for activity_date in sorted(activity_dates):
        if previous_date is None:
            streak = 1
        elif activity_date == previous_date + timedelta(days=1):
            streak += 1
        else:
            streak = 1

        longest_streak = max(longest_streak, streak)
        previous_date = activity_date

    return current_streak, longest_streak


def update_user_progress(user):
    activities = StudyActivity.objects.filter(user=user)

    totals = activities.aggregate(
        total_minutes=Sum("duration_minutes"),
        total_quizzes=Sum(
            "count",
            filter=Q(activity_type="quiz")
        ),
        total_flashcards=Sum(
            "count",
            filter=Q(activity_type="flashcard")
        )
    )

    current_streak, longest_streak = calculate_study_streak(user)

    progress, created = UserProgress.objects.get_or_create(
        user=user
    )

    progress.total_study_minutes = totals["total_minutes"] or 0
    progress.total_quizzes = totals["total_quizzes"] or 0
    progress.total_flashcards_reviewed = totals["total_flashcards"] or 0
    progress.current_streak = current_streak
    progress.longest_streak = longest_streak

    progress.save()

    return progress
