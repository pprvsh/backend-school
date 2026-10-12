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
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source="department",
        write_only=True,
    )

    class Meta:
        model = Faculty
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "department",
            "department_id",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]