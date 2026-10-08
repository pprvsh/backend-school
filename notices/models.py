from django.db import models


class Notice(models.Model):

    class Category(models.TextChoices):
        ACADEMIC = "academic", "Academic"
        EVENT = "event", "Event"
        GENERAL = "general", "General"
        URGENT = "urgent", "Urgent"

    class PriorityLevel(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    content = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL,
    )

    priority_level = models.IntegerField(
        choices=PriorityLevel.choices,
        default=PriorityLevel.MEDIUM,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title