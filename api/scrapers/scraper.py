from abc import ABC, abstractmethod

class Scraper(ABC):
  @abstractmethod
  def scrape(self):
    pass
  
  def is_tech_role(self, job):
      # Need to be lowercase for case-insensitive search
      tech_keywords = ['developer', 'programmer', 'software', 'it', 'technical', 'data', 'devops', 'ai', 
                        'machine learning', 'ml', 'cloud', 'database', 'network', 'security', 'embedded',
                        'systems', 'web', 'mobile', 'frontend', 'backend', 'fullstack', "qa"]
      irrelevant_keywords = ['sales', 'marketing', 'hr', 'recruiter', 'legal']
      
      job_title = job['title'].lower()
      contains_tech_keyword = any(keyword in job_title for keyword in tech_keywords)
      contains_irrelevant_keyword = any(keyword in job_title for keyword in irrelevant_keywords)

      return contains_tech_keyword and not contains_irrelevant_keyword
  
  def filter_tech_jobs(self, jobs):
    return [job for job in jobs if self.is_tech_role(job)]
  
  @abstractmethod
  def transform_data(self, jobs):
    """
    Transforms scraped data into valid Job model instances
    """
    pass