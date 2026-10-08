from rest_framework import serializers

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "category",
            "priority_level",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]