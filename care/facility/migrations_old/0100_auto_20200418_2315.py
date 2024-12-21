from django.utils.translation import gettext_lazy as _
# Generated by Django 2.2.11 on 2020-04-18 17:45

from django.db import migrations, models

import care.utils.models.jsonfield


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0099_auto_20200418_2030"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalpatientregistration",
            name="countries_travelled",
            field=care.utils.models.jsonfield.JSONField(
                blank=True, null=True, verbose_name=_("Countries Patient has Travelled to")
            ),
        ),
        migrations.AddField(
            model_name="patientregistration",
            name="countries_travelled",
            field=care.utils.models.jsonfield.JSONField(
                blank=True, null=True, verbose_name=_("Countries Patient has Travelled to")
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatientregistration",
            name="countries_travelled_old",
            field=models.TextField(
                blank=True,
                editable=False,
                null=True,
                verbose_name=_("Countries Patient has Travelled to"),
            ),
        ),
        migrations.AlterField(
            model_name="patientregistration",
            name="countries_travelled_old",
            field=models.TextField(
                blank=True,
                editable=False,
                null=True,
                verbose_name=_("Countries Patient has Travelled to"),
            ),
        ),
    ]
