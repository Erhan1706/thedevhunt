from django.apps import AppConfig
from django.db.utils import OperationalError
import os
import json

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # Create a periodic task to scrape vacancies if it does not exist
    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        from django.core.management import call_command
        from .tasks import async_scrape_all_vacancies

        prod = os.environ.get('DJANGO_PRODUCTION', '') != 'False'
        task_name = "async_scrape_all_vacancies"        
        try:
            if not PeriodicTask.objects.filter(name=task_name).exists():
                schedule, _ = IntervalSchedule.objects.get_or_create(
                    every= 2 if not prod else 4,
                    period=IntervalSchedule.MINUTES if not prod else IntervalSchedule.HOURS,
                )

                PeriodicTask.objects.create(
                    name=task_name,
                    task=f"api.tasks.{task_name}",
                    interval=schedule,
                    args=json.dumps([]),
                    kwargs=json.dumps({}),
                    enabled=True,
                )
                print(f"Created periodic task: {task_name}")
        except OperationalError:
            # Prevent issues during initial migration setup
            pass