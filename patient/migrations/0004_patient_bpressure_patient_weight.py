# Generated by Django 4.2.4 on 2023-08-28 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_rename_service_treatment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='BPressure',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
