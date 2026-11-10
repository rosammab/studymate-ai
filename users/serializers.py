from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    phone_number = serializers.CharField(write_only=True)
    university = serializers.CharField(write_only=True)
    course = serializers.CharField(write_only=True)
    year_of_study = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    country = serializers.CharField(write_only=True)
    board = serializers.CharField(write_only=True)
    bio = serializers.CharField(write_only=True, required=False)
    study_goal = serializers.CharField(write_only=True, required=False)
    preferred_language = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "university",
            "course",
            "year_of_study",
            "state",
            "country",
            "board",
            "bio",
            "study_goal",
            "preferred_language",
        ]

    def create(self, validated_data):

        profile_data = {
            "phone_number": validated_data.pop("phone_number"),
            "university": validated_data.pop("university"),
            "course": validated_data.pop("course"),
            "year_of_study": validated_data.pop("year_of_study"),
            "state": validated_data.pop("state"),
            "country": validated_data.pop("country"),
            "board": validated_data.pop("board"),
            "bio": validated_data.pop("bio", ""),
            "study_goal": validated_data.pop("study_goal", ""),
            "preferred_language": validated_data.pop("preferred_language"),
        }

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(
            user=user,
            **profile_data
        )

        return user

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = UserProfile

        fields = [
            "username",
            "email",
            "phone_number",
            "university",
            "course",
            "year_of_study",
            "state",
            "country",
            "board",
            "bio",
            "study_goal",
            "preferred_language",
        ]

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    new_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_new_password(self, value):
        from django.contrib.auth.password_validation import (
            validate_password,
        )

        validate_password(value)
        return value