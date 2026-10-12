from rest_framework import viewsets

from .serializers import FacultySerializer
from .selector import get_all_faculty
from .services import create_faculty


class FacultyViewSet(viewsets.ModelViewSet):
    serializer_class = FacultySerializer

    def get_queryset(self):
        return get_all_faculty()

    def perform_create(self, serializer):
        serializer.instance = create_faculty(serializer.validated_data)