# Generated by Django 4.2.6 on 2023-12-08 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FrontEnd', '0031_labprescriptionhistorydb_lab'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospitalnewdb',
            old_name='Password',
            new_name='H_Password',
        ),
        migrations.RenameField(
            model_name='hospitalnewdb',
            old_name='Username',
            new_name='H_Username',
        ),
    ]
