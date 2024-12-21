from django.utils.translation import gettext_lazy as _
# Generated by Django 2.2.11 on 2022-04-15 14:02

import uuid

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0286_auto_20220316_2004"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dailyround",
            name="admitted_to",
        ),
        migrations.RemoveField(
            model_name="dailyround",
            name="bed",
        ),
        migrations.RemoveField(
            model_name="patientconsultation",
            name="admitted_to",
        ),
        migrations.CreateModel(
            name="ConsultationBed",
            fields=[
                (
                    "id",
                    models.AutoField(
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
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField(blank=True, default=None, null=True)),
                ("meta", django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                (
                    "bed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="facility.Bed"
                    ),
                ),
                (
                    "consultation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="facility.PatientConsultation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
