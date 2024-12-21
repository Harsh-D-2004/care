from django.utils.translation import gettext_lazy as _
# Generated by Django 2.2.11 on 2020-07-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0129_auto_20200706_1912"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalpatientregistration",
            name="is_antenatal",
            field=models.BooleanField(
                default=False, verbose_name=_("Does the patient require Prenatal Care ?")
            ),
        ),
        migrations.AddField(
            model_name="patientregistration",
            name="is_antenatal",
            field=models.BooleanField(
                default=False, verbose_name=_("Does the patient require Prenatal Care ?")
            ),
        ),
        migrations.AlterField(
            model_name="facilityrelatedsummary",
            name="s_type",
            field=models.CharField(
                choices=[
                    ("FacilityCapacity", "FacilityCapacity"),
                    ("PatientSummary", "PatientSummary"),
                ],
                max_length=100,
            ),
        ),
    ]
