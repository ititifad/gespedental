# Generated by Django 4.2.4 on 2023-08-24 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medicalhistory',
            options={'verbose_name_plural': 'Medical History'},
        ),
        migrations.RemoveField(
            model_name='patient',
            name='user',
        ),
    ]
