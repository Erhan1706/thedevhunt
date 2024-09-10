from django.core.management.base import BaseCommand
from api.tasks import async_scrape_all_vacancies

class Command(BaseCommand):
  help = 'Run celery tasks'

  def handle(self, *args, **options):
    async_scrape_all_vacancies.delay()
    #ScraperFactory.get_scraper("thales").get_vacancies()