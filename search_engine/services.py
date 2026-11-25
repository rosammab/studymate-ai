
from django.db.models import Q

from notes.models import Note
from documents.models import StudyDocument
from quizzes.models import Quiz
from flashcards.models import FlashcardSet, Flashcard


def format_result(source, obj, title, description):
    """
    Format search results into a consistent response structure.
    """

    return {
        "source": source,
        "id": obj.id,
        "title": title or "",
        "description": description or "",
        "created_at": obj.created_at,
    }


# ==========================================
# SEARCH NOTES
# ==========================================

def search_notes(user, query):

    notes = Note.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    ).order_by("-created_at")[:50]

    return [
        format_result(
            "note",
            note,
            note.title,
            (note.content or "")[:300]
        )
        for note in notes
    ]


# ==========================================
# SEARCH DOCUMENTS
# ==========================================

def search_documents(user, query):

    documents = StudyDocument.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(extracted_text__icontains=query)
    ).order_by("-created_at")[:50]

    return [
        format_result(
            "document",
            document,
            document.title,
            (document.extracted_text or "")[:300]
        )
        for document in documents
    ]


# ==========================================
# SEARCH QUIZZES
# ==========================================

def search_quizzes(user, query):

    quizzes = Quiz.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(questions__question_text__icontains=query)
    ).distinct().order_by("-created_at")[:50]

    return [
        format_result(
            "quiz",
            quiz,
            quiz.title,
            quiz.description
        )
        for quiz in quizzes
    ]


# ==========================================
# SEARCH FLASHCARD SETS AND CARDS
# ==========================================

def search_flashcards(user, query):

    # Search flashcard sets by title and description.
    flashcard_sets = FlashcardSet.objects.filter(
        user=user
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    ).order_by("-created_at")[:50]

    set_results = [
        format_result(
            "flashcard_set",
            flashcard_set,
            flashcard_set.title,
            flashcard_set.description
        )
        for flashcard_set in flashcard_sets
    ]

    # Search individual flashcards.
    # flashcard_set is the actual ForeignKey field.
    cards = Flashcard.objects.filter(
        flashcard_set__user=user
    ).filter(
        Q(question__icontains=query) |
        Q(answer__icontains=query)
    ).select_related(
        "flashcard_set"
    ).order_by("-created_at")[:50]

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


# ==========================================
# GLOBAL SEARCH
# ==========================================

def global_search(user, query):

    results = []

    results.extend(search_notes(user, query))
    results.extend(search_documents(user, query))
    results.extend(search_quizzes(user, query))
    results.extend(search_flashcards(user, query))

    # Sort all results by creation date.
    results.sort(
        key=lambda item: item["created_at"],
        reverse=True
    )

    return results


# ==========================================
# RECOMMENDATIONS
# ==========================================

def get_recommendations(user, limit=10):
    """
    MVP recommendation strategy:
    Return the user's most recently created learning materials.
    """

    recommendations = []

    # Recent notes
    notes = Note.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]

    for note in notes:
        recommendations.append(
            format_result(
                "note",
                note,
                note.title,
                (note.content or "")[:300]
            )
        )

    # Recent documents
    documents = StudyDocument.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]

    for document in documents:
        recommendations.append(
            format_result(
                "document",
                document,
                document.title,
                (document.extracted_text or "")[:300]
            )
        )

    # Recent quizzes
    quizzes = Quiz.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]

    for quiz in quizzes:
        recommendations.append(
            format_result(
                "quiz",
                quiz,
                quiz.title,
                quiz.description
            )
        )

    # Recent flashcard sets
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

    # Sort all recommendations by creation date.
    recommendations.sort(
        key=lambda item: item["created_at"],
        reverse=True
    )

    return recommendations[:limit]
