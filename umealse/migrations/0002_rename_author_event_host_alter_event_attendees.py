# Generated by Django 4.1.5 on 2023-02-02 13:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("umealse", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="author",
            new_name="host",
        ),
        migrations.AlterField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
