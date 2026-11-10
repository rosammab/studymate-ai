from rest_framework import serializers
from .models import (
    Quiz,
    Question,
    QuizOption,
    QuizAttempt,
    QuizAnswer,
)


class QuizSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    question_count = serializers.IntegerField(
        source="questions.count",
        read_only=True
    )

    class Meta:
        model = Quiz
        fields = [
            "id", "user", "title", "description",
            "question_count", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "user", "question_count",
            "created_at", "updated_at",
        ]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Quiz title cannot be empty."
            )
        return value


class QuizOptionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ["id", "option_text"]


class QuestionPublicSerializer(serializers.ModelSerializer):
    options = QuizOptionPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "marks", "options"]


class QuizDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    questions = QuestionPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id", "user", "title", "description",
            "questions", "created_at"
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id", "quiz", "question_text", "marks", "created_at"
        ]
        read_only_fields = ["id", "quiz", "created_at"]

    def validate_question_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Question cannot be empty."
            )
        return value

    def validate_marks(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Marks must be at least 1."
            )
        return value


class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ["id", "question", "option_text", "is_correct"]
        read_only_fields = ["id", "question"]

    def validate_option_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Option text cannot be empty."
            )
        return value


class QuizAnswerResultSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(
        source="question.question_text",
        read_only=True
    )
    selected_option_text = serializers.CharField(
        source="selected_option.option_text",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = QuizAnswer
        fields = [
            "id", "question", "question_text",
            "selected_option", "selected_option_text", "is_correct",
        ]


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(
        source="quiz.title",
        read_only=True
    )
    answers = QuizAnswerResultSerializer(many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = [
            "id", "quiz", "quiz_title", "score",
            "total_marks", "submitted_at", "answers",
        ]