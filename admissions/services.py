from .models import AdmissionInquiry


def process_admission_inquiry(data: dict) -> AdmissionInquiry:
    inquiry = AdmissionInquiry.objects.create(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        grade=data["grade"],
        message=data["message"],
    )

    return inquiry