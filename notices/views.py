from rest_framework import viewsets

from .models import Notice
from .serializers import NoticeSerializer
from .selectors import get_all_notices


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return get_all_notices()