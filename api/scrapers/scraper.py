from abc import ABC, abstractmethod
from jobs.models import Job
from django.utils import timezone
from django.db import transaction


# Abstract class for scraping job listings. All scrapers for specific websites should inherit from this class
class Scraper(ABC):
  eu_countries = ["Netherlands", "United Kingdom", "Germany", "France", "Austria", "Ireland", "Czech Republic", 
                        "Denmark", "Belgium", "Croatia", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden",
                        "Cyprus", "Estonia", "Finland", "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Turkey",
                        "Iceland", "Latvia", "Lithuania", "Luxembourg", "Malta", "Russia", "Serbia", "Slovakia", 
                        "Ukraine", "Slovenia", "Belarus", "Bosnia and Herzegovina", "Moldova", "Montenegro",
                        "San Marino", "Vatican City", "Liechtenstein", "Albania","Kosovo", "Monaco", "North Macedonia", "Andorra"]

  @abstractmethod
  def scrape(self):
    pass
  
  def is_tech_role(self, job):
      # Need to be lowercase for case-insensitive search
      tech_keywords = ['developer', 'programmer', 'software', 'it', 'technical', 'data', 'devops', 'ai', 
                        'machine learning', 'ml', 'cloud', 'database', 'network', 'security', 'embedded',
                        'systems', 'web', 'mobile', 'frontend', 'backend', 'fullstack', "qa"]
      irrelevant_keywords = ['sales', 'marketing', 'hr', 'recruiter', 'legal', 'ambassador', 'business', 'finance']
      
      job_title = job['title'].lower()
      contains_tech_keyword = any(keyword in job_title for keyword in tech_keywords)
      contains_irrelevant_keyword = any(keyword in job_title for keyword in irrelevant_keywords)

      return contains_tech_keyword and not contains_irrelevant_keyword
  
  def filter_tech_jobs(self, jobs):
    return [job for job in jobs if self.is_tech_role(job)]
  
  @abstractmethod
  def transform_data(self, jobs):
    """
    Transforms scraped data into valid Job instances
    """
    pass

  @abstractmethod
  def get_vacancies(self):
    """
    Returns a list of valid Job objects in order to save them to the db
    """
    pass


  def save_or_update_job(self, job):
    """ Save a job in the database. If it exists, update the fields to newest version """ 
    existing_job = Job.objects.filter(slug=job.slug, company=job.company).first()
    if existing_job:
      existing_job.title = job.title
      existing_job.role = job.role
      existing_job.technologies = job.technologies
      existing_job.company = job.company
      existing_job.location = job.location
      existing_job.link_to_apply = job.link_to_apply
      existing_job.created_at = job.created_at
      existing_job.employment_type = job.employment_type
      existing_job.remote = job.remote
      existing_job.description = job.description
      existing_job.last_modified = timezone.now()
      existing_job.save()
    else:
      job.save()

  def delete_non_scraped_jobs(self, scraped_job_identifiers):
    """ Delete jobs that are not in the scraped_job_identifiers list """
    if not scraped_job_identifiers:
      print("No jobs were scraped")
      return
    relevant_jobs = Job.objects.filter(company__iexact=scraped_job_identifiers[0][1])
    deleted_jobs = relevant_jobs.exclude(
        slug__in=[identifier[0] for identifier in scraped_job_identifiers],
        company__in=[identifier[1] for identifier in scraped_job_identifiers]
    )
    print(f"Deleting {deleted_jobs.count()} jobs")
    deleted_jobs.delete()
  
  @transaction.atomic
  def update_db(self, jobs):
    scraped_job_identifiers = [(job.slug, job.company) for job in jobs]
    
    # Update or save scraped jobs
    for job in jobs:
        self.save_or_update_job(job)
    
    # Delete jobs that weren't scraped
    self.delete_non_scraped_jobs(scraped_job_identifiers)
