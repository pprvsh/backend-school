import pytest
from rest_framework.test import APIClient

from admissions.models import AdmissionInquiry


@pytest.mark.django_db
def test_create_admission_returns_201():
    client = APIClient()

    payload = {
        "parent_name": "Sita Thapa",
        "email": "sita@example.com",
        "phone": "9800000001",
        "student_grade": "Grade 1",
    }

    response = client.post(
        "/api/v1/admissions/",
        payload,
        format="json",
    )

    # Check the HTTP response.
    assert response.status_code == 201

    # Check that the API saved the inquiry.
    assert AdmissionInquiry.objects.count() == 1

    inquiry = AdmissionInquiry.objects.get(
        email="sita@example.com"
    )

    assert inquiry.parent_name == "Sita Thapa"
    assert inquiry.student_grade == "Grade 1"