from django.utils.translation import gettext_lazy as _
# Generated by Django 2.2.11 on 2020-09-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0183_shiftingrequest_is_kasp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpatientregistration",
            name="fit_for_blood_donation",
            field=models.BooleanField(
                default=False,
                null=True,
                verbose_name=_("Is Patient fit for donating Blood"),
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatientregistration",
            name="test_type",
            field=models.IntegerField(
                choices=[
                    (10, "UNK"),
                    (20, "ANTIGEN"),
                    (30, "RTPCR"),
                    (40, "CBNAAT"),
                    (50, "TRUENAT"),
                ],
                default=10,
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatientregistration",
            name="will_donate_blood",
            field=models.BooleanField(
                default=None,
                null=True,
                verbose_name=_("Is Patient Willing to donate Blood"),
            ),
        ),
        migrations.AlterField(
            model_name="patientregistration",
            name="fit_for_blood_donation",
            field=models.BooleanField(
                default=False,
                null=True,
                verbose_name=_("Is Patient fit for donating Blood"),
            ),
        ),
        migrations.AlterField(
            model_name="patientregistration",
            name="test_type",
            field=models.IntegerField(
                choices=[
                    (10, "UNK"),
                    (20, "ANTIGEN"),
                    (30, "RTPCR"),
                    (40, "CBNAAT"),
                    (50, "TRUENAT"),
                ],
                default=10,
            ),
        ),
        migrations.AlterField(
            model_name="patientregistration",
            name="will_donate_blood",
            field=models.BooleanField(
                default=None,
                null=True,
                verbose_name=_("Is Patient Willing to donate Blood"),
            ),
        ),
    ]
