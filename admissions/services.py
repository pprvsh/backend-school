
from django.db import transaction

from .models import AdmissionInquiry
from .task import send_admission_confirmation_email


def process_admission_inquiry(data: dict) -> AdmissionInquiry:
    inquiry = AdmissionInquiry.objects.create(
        parent_name=data["parent_name"],
        email=data["email"],
        phone=data["phone"],
        student_grade=data["student_grade"],
    )

    # Send the email asynchronously after the database commits.
    transaction.on_commit(
        lambda: send_admission_confirmation_email.delay(inquiry.id)
    )

    return inquiry
