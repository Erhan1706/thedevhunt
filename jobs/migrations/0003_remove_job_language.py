# Generated by Django 4.2.14 on 2024-08-05 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_job_last_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='language',
        ),
    ]
