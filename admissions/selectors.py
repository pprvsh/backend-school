from .models import AdmissionInquiry


def get_all_admission_inquiries():
    return AdmissionInquiry.objects.all()