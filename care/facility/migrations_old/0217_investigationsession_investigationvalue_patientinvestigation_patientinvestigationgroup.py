from django.utils.translation import gettext_lazy as _
# Generated by Django 2.2.11 on 2021-04-17 18:01

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0216_auto_20210201_2228"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvestigationSession",
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
                ("created_date", models.DateTimeField(auto_now_add=True, null=True)),
                ("modified_date", models.DateTimeField(auto_now=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("session", models.UUIDField(db_index=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PatientInvestigationGroup",
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
                ("created_date", models.DateTimeField(auto_now_add=True, null=True)),
                ("modified_date", models.DateTimeField(auto_now=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=500)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PatientInvestigation",
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
                ("created_date", models.DateTimeField(auto_now_add=True, null=True)),
                ("modified_date", models.DateTimeField(auto_now=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=500)),
                ("unit", models.TextField(blank=True, null=True)),
                ("ideal_value", models.TextField(blank=True, null=True)),
                ("min_value", models.FloatField(blank=True, default=None, null=True)),
                ("max_value", models.FloatField(blank=True, default=None, null=True)),
                (
                    "investigation_type",
                    models.CharField(
                        choices=[
                            ("Float", "Float"),
                            ("String", "String"),
                            ("Choice", "Choice"),
                        ],
                        default=None,
                        max_length=10,
                        null=True,
                    ),
                ),
                ("choices", models.TextField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(to="facility.PatientInvestigationGroup"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="InvestigationValue",
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
                ("created_date", models.DateTimeField(auto_now_add=True, null=True)),
                ("modified_date", models.DateTimeField(auto_now=True, null=True)),
                ("deleted", models.BooleanField(default=False)),
                ("value", models.FloatField(blank=True, default=None, null=True)),
                ("notes", models.TextField(blank=True, default=None, null=True)),
                (
                    "consultation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="facility.PatientConsultation",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="facility.PatientInvestigationGroup",
                    ),
                ),
                (
                    "investigation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="facility.PatientInvestigation",
                    ),
                ),
                (
                    "session_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="facility.InvestigationSession",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
