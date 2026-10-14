
from rest_framework import serializers

from .models import AdmissionInquiry


class AdmissionInquirySerializer(serializers.ModelSerializer):

    def validate_phone(self, value):
        """Accept only a 10-digit phone number."""
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain digits only."
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return value

    def validate_parent_name(self, value):
        """Reject unsafe characters and invalid parent names."""
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Parent name cannot be empty."
            )

        if any(ord(char) < 32 for char in value):
            raise serializers.ValidationError(
                "Parent name contains invalid control characters."
            )

        if any(char in "<>" for char in value):
            raise serializers.ValidationError(
                "Parent name contains invalid characters."
            )

        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Parent name must not contain numbers."
            )

        return value

    class Meta:
        model = AdmissionInquiry
        fields = [
            "id",
            "parent_name",
            "email",
            "phone",
            "student_grade",
            "status",
        ]
        read_only_fields = ["id", "status"]
