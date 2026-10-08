from rest_framework import serializers

from .models import AdmissionInquiry


class AdmissionInquirySerializer(serializers.ModelSerializer):
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