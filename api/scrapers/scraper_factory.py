from .scraper_jetbrains import JetbrainsScraper

class ScraperFactory:
    
    available_scrapers = {"jetbrains": JetbrainsScraper}

    @staticmethod
    def get_scraper(scraper_name):
      if scraper_name in ScraperFactory.available_scrapers:
        return ScraperFactory.available_scrapers[scraper_name]()
      else:
        raise Exception(f"Scraper not available for {scraper_name}")
      
    def is_tech_role(self, job):
      # Need to be lowercase for case-insensitive search
      tech_keywords = ['developer', 'programmer', 'software', 'it', 'technical', 'data', 'devops', 'ai', 
                        'machine learning', 'ml', 'cloud', 'database', 'network', 'security', 'embedded',
                        'systems', 'web', 'mobile', 'frontend', 'backend', 'fullstack', "qa"]
      
      for role in job['role']:
          if any(keyword in role.lower() for keyword in tech_keywords):
              return True
      return False
  
    def filter_tech_jobs(self, jobs):
      return [job for job in jobs if self.is_tech_role(job)]