from .models import Faculty


def create_faculty(data: dict) -> Faculty:
    return Faculty.objects.create(**data)
