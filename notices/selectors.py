from .models import Notice


def get_all_notices():
    return Notice.objects.all().order_by("-created_at")


def get_recent_notices(limit=10):
    return Notice.objects.all().order_by("-created_at")[:limit]


def get_notices_by_category(category):
    return Notice.objects.filter(
        category=category
    ).order_by("-created_at")


def get_high_priority_notices():
    return Notice.objects.filter(
        priority_level="high"
    ).order_by("-created_at")
    from .models import Notice


def get_all_notices():
    return Notice.objects.all()


def get_recent_notices():
    return Notice.objects.order_by("-created_at")


def get_high_priority_notices():
    return Notice.objects.filter(
        priority_level=Notice.PriorityLevel.HIGH
    ).order_by("-created_at")