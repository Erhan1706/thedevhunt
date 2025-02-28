from django.core.management.base import BaseCommand
from jobs.models import Job
from api.scrapers.scraper_factory import ScraperFactory

class Command(BaseCommand):
  help = 'Fetch jobs from API and saves them to database'

  def handle(self, *args, **options):

    ScraperFactory.get_scraper("uber").get_vacancies()