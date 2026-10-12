from .models import Notice


def create_notice(data: dict) -> Notice:
    return Notice.objects.create(**data)
