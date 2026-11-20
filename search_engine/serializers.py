
from rest_framework import serializers


class SearchResultSerializer(serializers.Serializer):
    source = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()


class RecommendationSerializer(serializers.Serializer):
    source = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    created_at = serializers.DateTimeField()
