# Generated by Django 4.2.14 on 2024-08-05 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]