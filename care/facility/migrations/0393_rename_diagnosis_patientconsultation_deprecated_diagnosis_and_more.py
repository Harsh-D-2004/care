from django.utils.translation import gettext_lazy as _
# Generated by Django 4.2.5 on 2023-11-03 07:49

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import care.facility.models.mixins.permissions.patient


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("facility", "0392_alter_dailyround_consciousness_level"),
    ]

    def populate_consultation_diagnosis(apps, schema_editor):
        PatientConsultation = apps.get_model("facility", "PatientConsultation")
        ConsultationDiagnosis = apps.get_model("facility", "ConsultationDiagnosis")

        objects = []

        for consultation in PatientConsultation.objects.all():
            processed_diagnosis_ids = []  # to skip duplicates if any
            principal_diagnosis_id = consultation.deprecated_icd11_principal_diagnosis

            # confirmed diagnoses
            for diagnosis_id in consultation.deprecated_icd11_diagnoses:
                if diagnosis_id in processed_diagnosis_ids:
                    continue
                processed_diagnosis_ids.append(diagnosis_id)
                objects.append(
                    ConsultationDiagnosis(
                        is_migrated=True,
                        consultation=consultation,
                        diagnosis_id=diagnosis_id,
                        verification_status="confirmed",
                        is_principal=diagnosis_id == principal_diagnosis_id,
                    )
                )

            # provisional diagnoses
            for diagnosis_id in consultation.deprecated_icd11_provisional_diagnoses:
                if diagnosis_id in processed_diagnosis_ids:
                    continue
                processed_diagnosis_ids.append(diagnosis_id)
                objects.append(
                    ConsultationDiagnosis(
                        is_migrated=True,
                        consultation=consultation,
                        diagnosis_id=diagnosis_id,
                        verification_status="provisional",
                        is_principal=diagnosis_id == principal_diagnosis_id,
                    )
                )

        ConsultationDiagnosis.objects.bulk_create(objects, batch_size=2000)

    operations = [
        migrations.RenameField(
            model_name="patientconsultation",
            old_name="diagnosis",
            new_name="deprecated_diagnosis",
        ),
        migrations.RenameField(
            model_name="patientconsultation",
            old_name="icd11_diagnoses",
            new_name="deprecated_icd11_diagnoses",
        ),
        migrations.RenameField(
            model_name="patientconsultation",
            old_name="icd11_principal_diagnosis",
            new_name="deprecated_icd11_principal_diagnosis",
        ),
        migrations.RenameField(
            model_name="patientconsultation",
            old_name="icd11_provisional_diagnoses",
            new_name="deprecated_icd11_provisional_diagnoses",
        ),
        migrations.CreateModel(
            name="ConsultationDiagnosis",
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
                    "verification_status",
                    models.CharField(
                        choices=[
                            ("unconfirmed", "Unconfirmed"),
                            ("provisional", "Provisional"),
                            ("differential", "Differential"),
                            ("confirmed", "Confirmed"),
                            ("refuted", "Refuted"),
                            ("entered-in-error", "Entered in Error"),
                        ],
                        max_length=20,
                    ),
                ),
                ("is_principal", models.BooleanField(default=False)),
                (
                    "is_migrated",
                    models.BooleanField(
                        default=False,
                        help_text=_("This field is to throw caution to data that was previously ported over"),
                    ),
                ),
                (
                    "consultation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diagnoses",
                        to="facility.patientconsultation",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "diagnosis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="facility.icd11diagnosis",
                    ),
                ),
            ],
            bases=(
                models.Model,
                care.facility.models.mixins.permissions.patient.ConsultationRelatedPermissionMixin,
            ),
        ),
        migrations.AddConstraint(
            model_name="consultationdiagnosis",
            constraint=models.UniqueConstraint(
                fields=("consultation", "diagnosis"),
                name="unique_diagnosis_per_consultation",
            ),
        ),
        migrations.AddConstraint(
            model_name="consultationdiagnosis",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_principal", True)),
                fields=("consultation", "is_principal"),
                name="unique_principal_diagnosis",
            ),
        ),
        migrations.AddConstraint(
            model_name="consultationdiagnosis",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("is_principal", False),
                    models.Q(
                        ("verification_status__in", ["refuted", "entered-in-error"]),
                        _negated=True,
                    ),
                    _connector="OR",
                ),
                name="refuted_or_entered_in_error_diagnosis_cannot_be_principal",
            ),
        ),
        migrations.RunPython(
            populate_consultation_diagnosis, reverse_code=migrations.RunPython.noop
        ),
    ]
