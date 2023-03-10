from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Event.Status.PUBLISHED)


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    attendees = models.ManyToManyField(User, blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    event_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    private = models.BooleanField(default=False)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PUBLISHED
    )

    objects = models.Manager()
    published = PublishedManager()

    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ["-event_date"]
        indexes = [
            models.Index(fields=["-event_date"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("event_detail", args=[self.id])


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="users/", blank=True)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}"

    def get_friend_requests(self):
        return Friendship.objects.filter(to_user=self)


class Friendship(models.Model):
    from_user = models.ForeignKey(
        Profile, related_name="from_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        Profile, related_name="to_user", on_delete=models.CASCADE
    )
