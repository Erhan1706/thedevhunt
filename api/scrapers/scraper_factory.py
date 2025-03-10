from . import *
from .scraper_registry import registry 

class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_name):
      scraper_cls = registry.get(scraper_name)
      if scraper_cls:
          return scraper_cls()
      else:
          raise Exception(f"Scraper not available for '{scraper_name}'")

    @staticmethod
    def get_all_scrapers():
      return list(registry.keys())