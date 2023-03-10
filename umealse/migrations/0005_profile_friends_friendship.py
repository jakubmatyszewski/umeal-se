# Generated by Django 4.2b1 on 2023-02-20 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("umealse", "0004_alter_event_tags_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="friends",
            field=models.ManyToManyField(blank=True, to="umealse.profile"),
        ),
        migrations.CreateModel(
            name="Friendship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "from_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="from_user",
                        to="umealse.profile",
                    ),
                ),
                (
                    "to_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_user",
                        to="umealse.profile",
                    ),
                ),
            ],
        ),
    ]
