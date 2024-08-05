from django.core.management.base import BaseCommand
from jobs.models import Job
import requests
from django.urls import reverse

class Command(BaseCommand):
  help = 'Fetch jobs from API and saves them to database'

  def handle(self, *args, **options):
    # Make a GET request to the getJobs endpoint
    response = requests.get(f"http://127.0.0.1:8000/{reverse('getJobsApi')}")

    if response.status_code == 200:
        # The request was successful
        jobs_data = response.json()
        # Process the jobs_data as needed
        self.stdout.write(self.style.SUCCESS('Successfully fetched jobs'))
    else:
        self.stdout.write(self.style.ERROR(f'Failed to fetch jobs. Status code: {response.status_code}'))
