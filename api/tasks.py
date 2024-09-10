from celery import shared_task
from .scrapers.scraper_factory import ScraperFactory 

@shared_task
def async_scrape_vacancies(scraper_name):
    scraper = ScraperFactory.get_scraper(scraper_name)
    scraper.get_vacancies()

@shared_task
def async_scrape_all_vacancies():
    scraper_names = ScraperFactory.get_all_scrapers()
    
    for scraper_name in scraper_names:
        async_scrape_vacancies.delay(scraper_name) 