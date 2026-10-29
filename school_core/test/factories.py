import factory
from django.contrib.auth import get_user_model

from admissions.models import AdmissionInquiry


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"testuser{n}")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.username}@example.com"
    )
    password = factory.PostGenerationMethodCall(
        "set_password", "TestPassword123"
    )


class AdmissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdmissionInquiry

    parent_name = factory.Faker("name")
    email = factory.Sequence(
        lambda n: f"parent{n}@example.com"
    )
    phone = factory.Sequence(lambda n: f"980000{n:04d}")
    student_grade = "Grade 1"
    status = "pending"