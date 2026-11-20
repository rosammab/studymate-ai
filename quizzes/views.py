
from django.db import transaction
from django.shortcuts import get_object_or_404
from progress.services import create_study_activity
from notifications.services import create_user_notification


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
    QuizSubmissionSerializer
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
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

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

        # Validate request using serializer
        submission_serializer = QuizSubmissionSerializer(
            data=request.data
        )

        submission_serializer.is_valid(
            raise_exception=True
        )

        answers = submission_serializer.validated_data["answers"]

        # Get quiz belonging to logged-in user
        quiz = get_object_or_404(
            Quiz,
            id=quiz_id,
            user=request.user
        )

        # Get quiz questions and options
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

        total_marks = sum(
            question.marks
            for question in questions.values()
        )

        # Validate submitted answers
        for answer in answers:

            question_id = answer["question"]
            option_id = answer.get("selected_option")

            if question_id not in questions:
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

            # Allow unanswered questions
            if option_id is None:
                submitted[question_id] = None
                continue

            # Check whether option belongs to question
            option = next(
                (
                    opt
                    for opt in question.options.all()
                    if opt.id == option_id
                ),
                None
            )

            if option is None:
                return Response(
                    {
                        "error": (
                            "Selected option does not belong "
                            "to this question."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            submitted[question_id] = option

            if option.is_correct:
                score += question.marks

        # Save attempt, progress and notification atomically
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
                            if selected_option
                            else False
                        )
                    )
                )

            QuizAnswer.objects.bulk_create(answer_objects)

            # Update study progress
            create_study_activity(
                user=request.user,
                activity_type="quiz",
                count=1,
                duration_minutes=0
            )

            # Create notification
            create_user_notification(
                user=request.user,
                title="Quiz Completed",
                message=f"You successfully completed the quiz: {quiz.title}.",
                notification_type="quiz"
            )

        percentage = (
            round((score / total_marks) * 100, 2)
            if total_marks
            else 0
        )

        correct_answers = sum(
            1
            for option in submitted.values()
            if option and option.is_correct
        )

        return Response(
            {
                "message": "Quiz submitted successfully.",
                "attempt_id": attempt.id,
                "score": score,
                "total_marks": total_marks,
                "percentage": percentage,
                "correct_answers": correct_answers,
                "total_questions": len(questions),
                "progress_updated": True,
                "notification_created": True
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
