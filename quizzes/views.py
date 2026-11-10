
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Quiz,
    Question,
    QuizOption,
    QuizAttempt,
    QuizAnswer,
)

from .serializers import (
    QuizSerializer,
    QuizDetailSerializer,
    QuestionSerializer,
    QuizOptionSerializer,
    QuizAttemptSerializer,
)

from .permissions import IsQuizOwnerOrReadOnly


class QuizListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuizDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    permission_classes = [IsAuthenticated, IsQuizOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return QuizDetailSerializer
        return QuizSerializer


class QuestionListAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(
            quiz__user=self.request.user,
            quiz_id=self.kwargs["quiz_id"]
        )


class QuestionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        quiz = get_object_or_404(
            Quiz,
            id=self.kwargs["quiz_id"],
            user=self.request.user
        )
        serializer.save(quiz=quiz)


class QuizOptionCreateAPIView(generics.CreateAPIView):
    serializer_class = QuizOptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question,
            id=self.kwargs["question_id"],
            quiz__user=self.request.user
        )
        serializer.save(question=question)


class QuizSubmitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        answers = request.data.get("answers")

        if not isinstance(answers, list):
            return Response(
                {"error": "Answers must be a list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        quiz = get_object_or_404(Quiz, id=quiz_id)

        questions = {
            question.id: question
            for question in quiz.questions.prefetch_related("options")
        }

        if not questions:
            return Response(
                {"error": "This quiz has no questions."},
                status=status.HTTP_400_BAD_REQUEST
            )

        submitted = {}
        score = 0
        total_marks = sum(q.marks for q in questions.values())

        for answer in answers:
            if not isinstance(answer, dict):
                return Response(
                    {"error": "Each answer must be an object."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            question_id = answer.get("question_id")
            option_id = answer.get("selected_option_id")

            if type(question_id) is not int or question_id not in questions:
                return Response(
                    {"error": "Invalid question ID."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if question_id in submitted:
                return Response(
                    {"error": "Duplicate question answer."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            question = questions[question_id]

            if option_id is None:
                submitted[question_id] = None
                continue

            if type(option_id) is not int:
                return Response(
                    {"error": "Invalid option ID."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            option = next(
                (o for o in question.options.all() if o.id == option_id),
                None
            )

            if option is None:
                return Response(
                    {"error": "Selected option does not belong to this question."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            submitted[question_id] = option

            if option.is_correct:
                score += question.marks

        with transaction.atomic():
            attempt = QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                total_marks=total_marks
            )

            answer_objects = []

            for question_id, question in questions.items():
                selected_option = submitted.get(question_id)

                answer_objects.append(
                    QuizAnswer(
                        attempt=attempt,
                        question=question,
                        selected_option=selected_option,
                        is_correct=(
                            selected_option.is_correct
                            if selected_option else False
                        )
                    )
                )

            QuizAnswer.objects.bulk_create(answer_objects)

        percentage = (
            round((score / total_marks) * 100, 2)
            if total_marks else 0
        )

        return Response(
            {
                "message": "Quiz submitted successfully.",
                "attempt_id": attempt.id,
                "score": score,
                "total_marks": total_marks,
                "percentage": percentage,
                "correct_answers": sum(
                    1 for option in submitted.values()
                    if option and option.is_correct
                ),
                "total_questions": len(questions),
            },
            status=status.HTTP_201_CREATED
        )


class QuizAttemptListAPIView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = QuizAttempt.objects.filter(
            user=self.request.user
        ).select_related("quiz").prefetch_related("answers")

        quiz_id = self.request.query_params.get("quiz")

        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)

        return queryset


class QuizAttemptDetailAPIView(generics.RetrieveAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(
            user=self.request.user
        ).select_related("quiz").prefetch_related("answers")
