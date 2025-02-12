from . import *

class ScraperFactory:
    available_scrapers = {"jetbrains": JetbrainsScraper,
                          "booking": BookingScraper,
                          #"thales": ThalesScraper,
                          #"uber": UberScraper,
                          "accenture": AccentureScraper,
                          "visa": VisaSraper,
                          "optiver": OptiverScraper}

    @staticmethod
    def get_scraper(scraper_name):
      if scraper_name in ScraperFactory.available_scrapers:
        return ScraperFactory.available_scrapers[scraper_name]()
      else:
        raise Exception(f"Scraper not available for {scraper_name}")
      
    @staticmethod
    def get_all_scrapers():
      return ScraperFactory.available_scrapers.keys()