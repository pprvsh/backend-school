
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import AdmissionInquiry


@shared_task
def send_admission_confirmation_email(inquiry_id):
    inquiry = AdmissionInquiry.objects.get(id=inquiry_id)

    subject = "Admission Inquiry Received"

    message = (
        f"Dear {inquiry.parent_name},\n\n"
        "Thank you for submitting an admission inquiry.\n"
        f"Student grade: {inquiry.student_grade}\n"
        "Our admissions team will contact you soon.\n\n"
        "Regards,\nAdmissions Team"
    )

    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[inquiry.email],
        fail_silently=False,
    )
