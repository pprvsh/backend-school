from django.db import models


class AdmissionInquiry(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONTACTED = "contacted", "Contacted"
        RESOLVED = "resolved", "Resolved"

    parent_name = models.CharField(
        max_length=15,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=10,
    )

    student_grade = models.CharField(
        max_length=10,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return f"{self.parent_name} - {self.student_grade}"
