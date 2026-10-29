"""
Unit tests — Admission serializer validation.

These tests exercise serializer logic in isolation (no database needed).
Run with:  pytest -m unit
"""

import pytest
from admissions.serializers import AdmissionInquirySerializer


# ── Valid data ──────────────────────────────────────────────

@pytest.mark.unit
def test_serializer_accepts_valid_data():
    data = {
        "parent_name": "Sita Thapa",
        "email": "sita@example.com",
        "phone": "9800000001",
        "student_grade": "Grade 1",
    }
    serializer = AdmissionInquirySerializer(data=data)
    assert serializer.is_valid(), serializer.errors


# ── Phone validation ───────────────────────────────────────

@pytest.mark.unit
def test_phone_must_be_10_digits():
    data = {
        "parent_name": "Sita Thapa",
        "email": "sita@example.com",
        "phone": "12345",
        "student_grade": "Grade 1",
    }
    serializer = AdmissionInquirySerializer(data=data)
    assert not serializer.is_valid()
    assert "phone" in serializer.errors


@pytest.mark.unit
def test_phone_rejects_non_digit_characters():
    data = {
        "parent_name": "Sita Thapa",
        "email": "sita@example.com",
        "phone": "98000abc01",
        "student_grade": "Grade 1",
    }
    serializer = AdmissionInquirySerializer(data=data)
    assert not serializer.is_valid()
    assert "phone" in serializer.errors


# ── Parent-name validation ─────────────────────────────────

@pytest.mark.unit
def test_parent_name_rejects_html_tags():
    data = {
        "parent_name": "<script>alert(1)</script>",
        "email": "x@example.com",
        "phone": "9800000001",
        "student_grade": "Grade 1",
    }
    serializer = AdmissionInquirySerializer(data=data)
    assert not serializer.is_valid()
    assert "parent_name" in serializer.errors


@pytest.mark.unit
def test_parent_name_rejects_numbers():
    data = {
        "parent_name": "Ram123",
        "email": "x@example.com",
        "phone": "9800000001",
        "student_grade": "Grade 1",
    }
    serializer = AdmissionInquirySerializer(data=data)
    assert not serializer.is_valid()
    assert "parent_name" in serializer.errors


@pytest.mark.unit
def test_parent_name_rejects_blank():
    data = {
        "parent_name": "   ",
        "email": "x@example.com",
        "phone": "9800000001",
        "student_grade": "Grade 1",
    }
    serializer = AdmissionInquirySerializer(data=data)
    assert not serializer.is_valid()
    assert "parent_name" in serializer.errors


# ── Email validation ───────────────────────────────────────

@pytest.mark.unit
def test_invalid_email_rejected():
    data = {
        "parent_name": "Sita Thapa",
        "email": "not-an-email",
        "phone": "9800000001",
        "student_grade": "Grade 1",
    }
    serializer = AdmissionInquirySerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors


# ── Required fields ────────────────────────────────────────

@pytest.mark.unit
def test_missing_required_fields():
    serializer = AdmissionInquirySerializer(data={})
    assert not serializer.is_valid()
    for field in ("parent_name", "email", "phone", "student_grade"):
        assert field in serializer.errors
