from django.utils.translation import gettext_lazy as _
# Generated by Django 4.2.2 on 2023-07-18 05:00

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0371_metaicd11diagnosis_chapter_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetAvailabilityRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name=_("ID"),
                    ),
                ),
                (
                    "external_id",
                    models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
                ),
                (
                    "created_date",
                    models.DateTimeField(auto_now_add=True, db_index=True, null=True),
                ),
                (
                    "modified_date",
                    models.DateTimeField(auto_now=True, db_index=True, null=True),
                ),
                ("deleted", models.BooleanField(db_index=True, default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Not Monitored", "Not Monitored"),
                            ("Operational", "Operational"),
                            ("Down", "Down"),
                            ("Under Maintenance", "Under Maintenance"),
                        ],
                        default="Not Monitored",
                        max_length=20,
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="facility.asset"
                    ),
                ),
            ],
            options={
                "ordering": ["-timestamp"],
                "unique_together": {("asset", "timestamp")},
            },
        ),
    ]
