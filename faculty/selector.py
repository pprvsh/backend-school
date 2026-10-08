from .models import Faculty


def get_all_faculty():
    return Faculty.objects.select_related("department").all()


def get_active_faculty():
    return (
        Faculty.objects
        .filter(is_active=True)
        .select_related("department")
    )