from .models import AdmissionInquiry


def process_admission_inquiry(data: dict) -> AdmissionInquiry:
    inquiry = AdmissionInquiry.objects.create(
        parent_name=data["parent_name"],
        email=data["email"],
        phone=data["phone"],
        student_grade=data["student_grade"],
    )

    return inquiry