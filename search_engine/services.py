
from django.db.models import Q

from notes.models import Note
from documents.models import StudyDocument
from quizzes.models import Quiz
from flashcards.models import FlashcardSet, Flashcard


def format_result(source, obj, title, description):
    return {
        "source": source,
        "id": obj.id,
        "title": title,
        "description": description or "",
        "created_at": obj.created_at,
    }


def search_notes(user, query):
    notes = Note.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    ).order_by("-created_at")

    return [
        format_result(
            "note",
            note,
            note.title,
            note.content[:300]
        )
        for note in notes
    ]


def search_documents(user, query):
    documents = StudyDocument.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(extracted_text__icontains=query)
    ).order_by("-created_at")

    return [
        format_result(
            "document",
            document,
            document.title,
            document.extracted_text[:300]
        )
        for document in documents
    ]


def search_quizzes(user, query):
    quizzes = Quiz.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(questions__question_text__icontains=query)
    ).distinct().order_by("-created_at")

    return [
        format_result(
            "quiz",
            quiz,
            quiz.title,
            quiz.description
        )
        for quiz in quizzes
    ]


def search_flashcards(user, query):
    flashcard_sets = FlashcardSet.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(cards__question__icontains=query) |
        Q(cards__answer__icontains=query)
    ).distinct().order_by("-created_at")

    set_results = [
        format_result(
            "flashcard_set",
            flashcard_set,
            flashcard_set.title,
            flashcard_set.description
        )
        for flashcard_set in flashcard_sets
    ]

    cards = Flashcard.objects.filter(
        flashcard_set__user=user
    ).filter(
        Q(question__icontains=query) |
        Q(answer__icontains=query)
    ).select_related("flashcard_set").order_by("-created_at")

    card_results = [
        format_result(
            "flashcard",
            card,
            card.question[:200],
            card.answer[:300]
        )
        for card in cards
    ]

    return set_results + card_results


def global_search(user, query):
    results = []

    results.extend(search_notes(user, query))
    results.extend(search_documents(user, query))
    results.extend(search_quizzes(user, query))
    results.extend(search_flashcards(user, query))

    results.sort(
        key=lambda item: item["created_at"],
        reverse=True
    )

    return results


def get_recommendations(user, limit=10):
    """
    MVP recommendation strategy:
    Return the user's most recently created learning materials.
    """

    recommendations = []

    notes = Note.objects.filter(user=user).order_by("-created_at")[:limit]

    for note in notes:
        recommendations.append(
            format_result(
                "note", note, note.title, note.content[:300]
            )
        )

    documents = StudyDocument.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]

    for document in documents:
        recommendations.append(
            format_result(
                "document",
                document,
                document.title,
                document.extracted_text[:300]
            )
        )

    quizzes = Quiz.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]

    for quiz in quizzes:
        recommendations.append(
            format_result(
                "quiz", quiz, quiz.title, quiz.description
            )
        )

    flashcard_sets = FlashcardSet.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]

    for flashcard_set in flashcard_sets:
        recommendations.append(
            format_result(
                "flashcard_set",
                flashcard_set,
                flashcard_set.title,
                flashcard_set.description
            )
        )

    recommendations.sort(
        key=lambda item: item["created_at"],
        reverse=True
    )

    return recommendations[:limit]
