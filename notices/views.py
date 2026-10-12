from rest_framework import viewsets
from users.permission import IsAdminUserOrReadOnly
from .serializers import NoticeSerializer
from .selectors import get_all_notices
from .services import create_notice


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = NoticeSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        return get_all_notices()

    def perform_create(self, serializer):
        serializer.instance = create_notice(serializer.validated_data)
