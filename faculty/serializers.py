from rest_framework import serializers

from .models import Department, Faculty


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
        ]


class FacultySerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Faculty
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "department",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]