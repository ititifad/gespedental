# Generated by Django 4.2.4 on 2023-08-29 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_remove_medicalhistory_treatment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Investgation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewofSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='history',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='diagnosis',
            field=models.ManyToManyField(to='patient.diagnosis'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='examination',
            field=models.ManyToManyField(to='patient.examination'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='investgation',
            field=models.ManyToManyField(to='patient.investgation'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='medication',
            field=models.ManyToManyField(to='patient.medication'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='review_of_systems',
            field=models.ManyToManyField(to='patient.reviewofsystem'),
        ),
    ]
