# Generated by Django 4.2.14 on 2024-08-15 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_created_at_job_employment_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='role',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=400),
        ),
    ]