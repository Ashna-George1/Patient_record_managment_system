# Generated by Django 4.2.6 on 2023-12-07 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FrontEnd', '0029_labprescriptiondb_doctor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinedb',
            name='Doctor_Name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patientdetailsdb',
            name='Doctor_Name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
