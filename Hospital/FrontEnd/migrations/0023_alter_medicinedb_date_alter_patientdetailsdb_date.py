# Generated by Django 4.2.6 on 2023-11-28 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FrontEnd', '0022_alter_medicinedb_date_alter_patientdetailsdb_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicinedb',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patientdetailsdb',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
