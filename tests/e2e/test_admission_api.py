"""
End-to-end tests — Admission API endpoints.

These tests make real HTTP requests through Django's test client,
exercising the full stack: URL routing → permissions → serializer → service → DB.
Run with:  pytest -m e2e
"""

from unittest.mock import patch

import pytest

from admissions.models import AdmissionInquiry


# ── CREATE (POST) ──────────────────────────────────────────

@pytest.mark.e2e
@pytest.mark.django_db
@patch("admissions.services.send_admission_confirmation_email.delay")
def test_create_admission_returns_201(mock_task, api_client, sample_admission_data):
    """Anyone (unauthenticated) can submit an admission inquiry."""
    response = api_client.post(
        "/api/admissions/",
        sample_admission_data,
        format="json",
    )

    assert response.status_code == 201

    # Row was saved.
    assert AdmissionInquiry.objects.count() == 1
    inquiry = AdmissionInquiry.objects.first()
    assert inquiry.parent_name == "Sita Thapa"
    assert inquiry.student_grade == "Grade 1"


@pytest.mark.e2e
@pytest.mark.django_db
def test_create_admission_rejects_invalid_payload(api_client):
    """The API must reject payloads that fail serializer validation."""
    bad_payload = {
        "parent_name": "",
        "email": "bad",
        "phone": "123",
        "student_grade": "",
    }
    response = api_client.post(
        "/api/admissions/",
        bad_payload,
        format="json",
    )
    assert response.status_code == 400


# ── LIST (GET) — requires authentication ───────────────────

@pytest.mark.e2e
@pytest.mark.django_db
def test_list_admissions_requires_auth(api_client):
    """An unauthenticated GET to the list endpoint must be rejected."""
    response = api_client.get("/api/admissions/")
    assert response.status_code in (401, 403)


@pytest.mark.e2e
@pytest.mark.django_db
def test_list_admissions_as_admin(authenticated_client, saved_inquiry):
    """An admin user can list all admission inquiries."""
    response = authenticated_client.get("/api/admissions/")
    assert response.status_code == 200
    assert response.data["count"] >= 1


# ── DETAIL (GET) — single inquiry ──────────────────────────

@pytest.mark.e2e
@pytest.mark.django_db
def test_retrieve_admission_as_admin(authenticated_client, saved_inquiry):
    """An admin user can retrieve a single admission inquiry."""
    response = authenticated_client.get(
        f"/api/admissions/{saved_inquiry.id}/"
    )
    assert response.status_code == 200
    assert response.data["email"] == saved_inquiry.email


@pytest.mark.e2e
@pytest.mark.django_db
def test_retrieve_admission_unauthenticated(api_client, saved_inquiry):
    """An unauthenticated user cannot retrieve a single inquiry."""
    response = api_client.get(
        f"/api/admissions/{saved_inquiry.id}/"
    )
    assert response.status_code in (401, 403)
