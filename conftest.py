"""
Root conftest.py — shared fixtures available to all tests.
"""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from admissions.models import AdmissionInquiry

User = get_user_model()


@pytest.fixture
def api_client():
    """Unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """A staff/admin user for endpoints that require authentication."""
    return User.objects.create_user(
        username="admin_test",
        email="admin@test.com",
        password="StrongPass123!",
        is_staff=True,
    )


@pytest.fixture
def authenticated_client(api_client, admin_user):
    """DRF test client authenticated as an admin user."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def sample_admission_data():
    """Valid admission inquiry payload."""
    return {
        "parent_name": "Sita Thapa",
        "email": "sita@example.com",
        "phone": "9800000001",
        "student_grade": "Grade 1",
    }


@pytest.fixture
def saved_inquiry(db, sample_admission_data):
    """An AdmissionInquiry already persisted in the database."""
    return AdmissionInquiry.objects.create(**sample_admission_data)
