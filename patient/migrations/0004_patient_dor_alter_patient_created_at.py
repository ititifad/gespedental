# Generated by Django 4.2.4 on 2024-08-16 04:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_alter_patient_bpressure_alter_patient_dob_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='DOR',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
