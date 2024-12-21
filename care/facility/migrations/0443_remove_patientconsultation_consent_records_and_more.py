from django.utils.translation import gettext_lazy as _
# Generated by Django 4.2.10 on 2024-05-30 16:35

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils import timezone

import care.facility.models.mixins.permissions.patient


class Migration(migrations.Migration):
    def migrate_consents(apps, schema_editor):
        PatientConsultation = apps.get_model("facility", "PatientConsultation")
        PatientConsent = apps.get_model("facility", "PatientConsent")
        FileUpload = apps.get_model("facility", "FileUpload")
        consultations = PatientConsultation.objects.filter(
            consent_records__isnull=False
        )
        for consultation in consultations:
            for consent in consultation.consent_records:
                new_consent = PatientConsent.objects.create(
                    consultation=consultation,
                    type=consent.get("type", 5),
                    patient_code_status=(
                        consent.get("patient_code_status", 0)
                        if consent.get("type", 5) == 2
                        else None
                    ),
                    created_by=consultation.created_by,
                    archived=consent.get("deleted", False),
                    is_migrated=True,
                    created_date=consultation.modified_date,
                )

                old_id = consent.get("id")

                files = FileUpload.objects.filter(
                    associating_id=old_id,
                    file_type=7,
                )

                kwargs = {
                    "associating_id": new_consent.external_id,
                }

                if consent.get("deleted", False):
                    kwargs = {
                        **kwargs,
                        "is_archived": True,
                        "archived_datetime": timezone.now(),
                        "archive_reason": "Consent Record Archived",
                        "archived_by": consultation.created_by,
                    }

                files.update(**kwargs)

    def reverse_migrate(apps, schema_editor):
        PatientConsent = apps.get_model("facility", "PatientConsent")
        for consent in PatientConsent.objects.all():
            consultation = consent.consultation
            consultation.consent_records.append(
                {
                    "type": consent.type,
                    "deleted": consent.archived,
                    "id": str(consent.external_id),
                    "patient_code_status": consent.patient_code_status,
                }
            )
            consultation.save()

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "facility",
            "0442_remove_patientconsultation_unique_patient_no_within_facility",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientConsent",
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
                    "type",
                    models.IntegerField(
                        choices=[
                            (1, "Consent for Admission"),
                            (2, "Patient Code Status"),
                            (3, "Consent for Procedure"),
                            (4, "High Risk Consent"),
                            (5, "Others"),
                        ]
                    ),
                ),
                (
                    "patient_code_status",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (0, "Not Specified"),
                            (1, "Do Not Hospitalize"),
                            (2, "Do Not Resuscitate"),
                            (3, "Comfort Care Only"),
                            (4, "Active Treatment"),
                        ],
                        null=True,
                    ),
                ),
                ("archived", models.BooleanField(default=False)),
                ("archived_date", models.DateTimeField(blank=True, null=True)),
                (
                    "archived_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="archived_consents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "consultation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="facility.patientconsultation",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_consents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "is_migrated",
                    models.BooleanField(
                        default=False,
                        help_text=_("This field is to throw caution to data that was previously ported over"),
                    ),
                ),
            ],
            bases=(
                models.Model,
                care.facility.models.mixins.permissions.patient.ConsultationRelatedPermissionMixin,
            ),
        ),
        migrations.AddConstraint(
            model_name="patientconsent",
            constraint=models.UniqueConstraint(
                condition=models.Q(("archived", False)),
                fields=("consultation", "type"),
                name="unique_consultation_consent",
            ),
        ),
        migrations.AddConstraint(
            model_name="patientconsent",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    models.Q(("type", 2), _negated=True),
                    ("patient_code_status__isnull", False),
                    _connector="OR",
                ),
                name="patient_code_status_required",
            ),
        ),
        migrations.AddConstraint(
            model_name="patientconsent",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("type", 2), ("patient_code_status__isnull", True), _connector="OR"
                ),
                name="patient_code_status_not_required",
            ),
        ),
        migrations.RunPython(migrate_consents, reverse_code=reverse_migrate),
        migrations.RemoveField(
            model_name="patientconsultation",
            name="consent_records",
        ),
    ]
