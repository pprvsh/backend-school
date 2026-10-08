from rest_framework import viewsets

from .models import Faculty
from .serializers import FacultySerializer
from .selector import get_all_faculty


class FacultyViewSet(viewsets.ModelViewSet):
    serializer_class = FacultySerializer

    def get_queryset(self):
        return get_all_faculty()