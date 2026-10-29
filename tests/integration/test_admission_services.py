"""
Integration tests — Admission service layer.

These tests hit the database but mock external services (Celery tasks).
Run with:  pytest -m integration
"""

from unittest.mock import patch

import pytest

from admissions.models import AdmissionInquiry
from admissions.services import process_admission_inquiry


@pytest.mark.integration
@pytest.mark.django_db
@patch("admissions.services.send_admission_confirmation_email.delay")
def test_process_admission_inquiry_saves_data(mock_task, sample_admission_data):
    """The service must persist the inquiry and schedule a Celery email task."""
    inquiry = process_admission_inquiry(sample_admission_data)

    # Row was persisted.
    assert AdmissionInquiry.objects.count() == 1

    saved = AdmissionInquiry.objects.get(id=inquiry.id)
    assert saved.parent_name == "Sita Thapa"
    assert saved.email == "sita@example.com"
    assert saved.phone == "9800000001"
    assert saved.student_grade == "Grade 1"
    assert saved.status == "pending"


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
@patch("admissions.services.send_admission_confirmation_email.delay")
def test_process_admission_triggers_celery_task(mock_task, sample_admission_data):
    """After saving, the Celery task must be scheduled with the new inquiry's ID."""
    inquiry = process_admission_inquiry(sample_admission_data)

    mock_task.assert_called_once_with(inquiry.id)


@pytest.mark.integration
@pytest.mark.django_db
def test_admission_model_str():
    """The __str__ method should return 'parent_name - student_grade'."""
    inquiry = AdmissionInquiry.objects.create(
        parent_name="Ram Sharma",
        email="ram@example.com",
        phone="9800000000",
        student_grade="Grade 2",
    )
    assert str(inquiry) == "Ram Sharma - Grade 2"


@pytest.mark.integration
@pytest.mark.django_db
def test_admission_default_status_is_pending():
    """Newly created inquiries default to 'pending' status."""
    inquiry = AdmissionInquiry.objects.create(
        parent_name="Gita Devi",
        email="gita@example.com",
        phone="9800000002",
        student_grade="Grade 3",
    )
    assert inquiry.status == "pending"
