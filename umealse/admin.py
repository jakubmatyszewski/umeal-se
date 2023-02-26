from django.contrib import admin
from .models import Event, Profile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "host", "created", "event_date", "private", "status"]
    list_filter = ["status", "host", "created", "event_date", "private"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["host"]
    date_hierarchy = "event_date"
    ordering = ["event_date"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "photo"]
    raw_id_fields = ["user"]
