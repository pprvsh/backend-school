from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import AdmissionInquirySerializer
from .selectors import get_all_admission_inquiries
from .services import process_admission_inquiry


class AdmissionInquiryViewSet(viewsets.ModelViewSet):
    serializer_class = AdmissionInquirySerializer

    def get_queryset(self):
        return get_all_admission_inquiries()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        inquiry = process_admission_inquiry(serializer.validated_data)

        output_serializer = self.get_serializer(inquiry)

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )