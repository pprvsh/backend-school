from unittest.mock import patch

import pytest

from admissions.models import AdmissionInquiry
from admissions.services import process_admission_inquiry


@pytest.mark.django_db
@patch("admissions.services.send_admission_confirmation_email.delay")
def test_process_admission_inquiry_saves_data(mock_task):
    data = {
        "parent_name": "Ram Sharma",
        "email": "ram@example.com",
        "phone": "9800000000",
        "student_grade": "Grade 1",
    }

    inquiry = process_admission_inquiry(data)

    # Check that the inquiry was saved.
    assert AdmissionInquiry.objects.count() == 1

    saved_inquiry = AdmissionInquiry.objects.get(
        id=inquiry.id
    )

    # Check the saved information.
    assert saved_inquiry.parent_name == "Ram Sharma"
    assert saved_inquiry.email == "ram@example.com"
    assert saved_inquiry.phone == "9800000000"
    assert saved_inquiry.student_grade == "Grade 1"

    # Check that the Celery task was scheduled.
    mock_task.assert_called_once_with(inquiry.id)