from abc import ABC, abstractmethod
from jobs.models import Job
from django.utils import timezone
from django.db import transaction
import requests
from difflib import SequenceMatcher

KEYWORD_MAPPINGS = {
  'Software Development': [
      'software', 'developer', 'frontend', 'backend', 'fullstack', 'qa', 'technical lead', 'tech lead', 'engineering manager',
      'senior engineer', 'junior engineer', 'staff engineer', 'principal engineer', 'android', 'ios', 'mobile', 'web developer',
  ],
  'Data': [
      'data', 'analytics', 'data science', 'data lead', 'head of data', 'data engineer'
  ],
  'ML & AI': [
      'ml', 'machine learning', 'artificial intelligence', 'deep learning', 'nlp', 'computer vision', 'ai',
      'ml researcher', 'ar/vr'
  ],
  'Cloud & Infrastructure': ['cloud', 'infrastructure', 'devops', 'sre', 'site reliability', 'platform engineer',
                              'solutions architect', 'cloud architect', 'cloud engineer'],
  'IT & Support': ['it', 'support', 'information technology', 'field engineering', 'customer support'],
  'Product & Project Management': ['product manager', 'project manager', 'program manager', 'product owner',
      'scrum master', 'business analyst', 'product management'
  ],
  'Cybersecurity': ['security', 'cybersecurity', 'security lead'],
  'Hardware': ['hardware', 'hardware engineering', 'electrical engineering', 'system'],
  'Design': ['design', 'designer', 'creative', 'ux', 'ui', 'design lead'],
}

# Abstract class for scraping job listings. All scrapers for specific websites should inherit from this class
class Scraper(ABC):
  url = ""
  headers = {}
  payload = {}
  company = ""

  eu_countries = ["Netherlands", "UK", "United Kingdom", "Germany", "France", "Austria", "Ireland", "Czech Republic", 
                        "Denmark", "Belgium", "Croatia", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden",
                        "Cyprus", "Estonia", "Finland", "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Turkey",
                        "Iceland", "Latvia", "Lithuania", "Luxembourg", "Malta", "Russia", "Serbia", "Slovakia", 
                        "Ukraine", "Slovenia", "Belarus", "Bosnia and Herzegovina", "Moldova", "Montenegro",
                        "San Marino", "Vatican City", "Liechtenstein", "Albania","Kosovo", "Monaco", "North Macedonia", "Andorra"]

  def scrape(self, method="GET") -> dict:
    response = requests.request(method, self.url, headers=self.headers, data=self.payload, verify=False)
    if response.status_code == 200:
      try:
        data = response.json() 
        return data
      except ValueError:
        print(f"Response content for {self.company} is not valid JSON")
        raise ValueError(f"Response content for {self.company} is not valid JSON")
    else:
      raise Exception(f"Request for {self.url} failed with status code: {response.status_code}")
  
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
  
  def classify_role_smart(self, job_role: str) -> str:
    """
    Classify a job role using fuzzy matching and keyword detection
    """
    job_role_clean = job_role.lower().strip()
    
    # Check for keyword matches
    for category, keywords in KEYWORD_MAPPINGS.items():
        if any(keyword in job_role_clean for keyword in keywords):
            return category
    
    # Fallback to fuzzy matching against known examples
    best_match = None
    best_score = 0.6  # minimum similarity threshold

    for category, examples in KEYWORD_MAPPINGS.items():
        for example in examples:
            similarity = SequenceMatcher(None, job_role_clean, example.lower()).ratio()
            if similarity > best_score:
                best_score = similarity
                best_match = category
    
    return best_match or 'Other'

  def filter_tech_jobs(self, jobs):
    return [job for job in jobs if self.is_tech_role(job)]
  
  @abstractmethod
  def transform_data(self, jobs) -> list[Job]:
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

  @transaction.atomic
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
      existing_job.created_at = job.created_at if job.created_at else existing_job.created_at
      existing_job.employment_type = job.employment_type
      existing_job.remote = job.remote
      existing_job.description = job.description
      existing_job.last_modified = timezone.now()
      existing_job.save()
    else:
      if not job.created_at:
        job.created_at = timezone.now() 
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
  
  def update_db(self, jobs):
    scraped_job_identifiers = [(job.slug, job.company) for job in jobs]
    
    # Update or save scraped jobs
    for job in jobs:
        try:
          self.save_or_update_job(job)
        except Exception as e:
          print(f"Error saving job: {job.title}")
          print(f"Slug: {job.slug} (length: {len(job.slug)})")
          print(f"Company: {job.company} (length: {len(job.company)})")
          print(f"Location: {job.location}")
          print(f"Error: {str(e)}")
    
    # Delete jobs that weren't scraped
    self.delete_non_scraped_jobs(scraped_job_identifiers)
