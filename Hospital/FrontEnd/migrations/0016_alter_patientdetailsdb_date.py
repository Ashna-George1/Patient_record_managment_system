# Generated by Django 4.2.6 on 2023-11-28 09:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FrontEnd', '0015_alter_patientdetailsdb_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetailsdb',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 11, 28, 14, 32, 36, 639762)),
        ),
    ]
