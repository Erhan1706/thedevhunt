from abc import ABC, abstractmethod

class Scraper(ABC):
  @abstractmethod
  def scrape(self):
    pass
  
  @abstractmethod
  def filter_tech_jobs(self, jobs):
    pass