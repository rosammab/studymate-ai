
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .services import (
    global_search,
    search_notes,
    search_documents,
    search_quizzes,
    search_flashcards,
    get_recommendations,
)

from .serializers import (
    SearchResultSerializer,
    RecommendationSerializer,
)


class BaseSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    search_function = None

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response(
                {"error": "Please provide a search query using ?q=."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(query) > 100:
            return Response(
                {"error": "Search query cannot exceed 100 characters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = self.search_function(request.user, query)

        serializer = SearchResultSerializer(results, many=True)

        return Response({
            "query": query,
            "count": len(results),
            "results": serializer.data
        })


class GlobalSearchAPIView(BaseSearchAPIView):
    search_function = staticmethod(global_search)


class NoteSearchAPIView(BaseSearchAPIView):
    search_function = staticmethod(search_notes)


class DocumentSearchAPIView(BaseSearchAPIView):
    search_function = staticmethod(search_documents)


class QuizSearchAPIView(BaseSearchAPIView):
    search_function = staticmethod(search_quizzes)

class FlashcardSearchAPIView(BaseSearchAPIView):
    search_function = staticmethod(search_flashcards)


class RecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 10))
        except (TypeError, ValueError):
            return Response(
                {"error": "Limit must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if limit < 1 or limit > 50:
            return Response(
                {"error": "Limit must be between 1 and 50."},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = get_recommendations(
            request.user,
            limit=limit
        )

        serializer = RecommendationSerializer(
            results,
            many=True
        )

        return Response({
            "count": len(results),
            "recommendations": serializer.data
        })
