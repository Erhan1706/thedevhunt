from .scraper_jetbrains import JetbrainsScraper

class ScraperFactory:
    
    available_scrapers = {"jetbrains": JetbrainsScraper}

    @staticmethod
    def get_scraper(scraper_name):
      if scraper_name in ScraperFactory.available_scrapers:
        return ScraperFactory.available_scrapers[scraper_name]()
      else:
        raise Exception(f"Scraper not available for {scraper_name}")
      
   