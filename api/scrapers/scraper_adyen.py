from .scraper import Scraper
from jobs.models import Job
from geopy.geocoders import Nominatim
import html
from .scraper_registry import register_scraper

@register_scraper("adyen")
class AdyenScraper(Scraper):

  url = "https://boards-api.greenhouse.io/v1/boards/adyen/jobs?content=true"

  headers = {}
  payload = {}

  company = "Adyen"
  geolocator = Nominatim(user_agent="devhunt")

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      listing = Job(
        title= job['title'],
        slug= job['id'],
        role= job['departments'][0]['name'],
        company= self.company,
        location= [f"{job['location']['name']}, {job['country']}"],
        link_to_apply= job['absolute_url'],
        employment_type= 'FULL_TIME',
        remote = False,
        description = html.unescape(job['content']),
        created_at= job['updated_at']
      )
      result.append(listing)

    return result
  
  def filter_tech_jobs(self, jobs):
    revelevant_adyen_departments = {"Development", "Infrastructure", "Data Analytics", "Product Management",
                                    "Security", "UX"}
    return [job for job in jobs if job['departments'][0]['name'] in revelevant_adyen_departments]


  def filter_eu_jobs(self, jobs):
    """
    JSON response from Adyen API does not contain country information, so we need to geocode the city 
    """
    eu_jobs = []
    for job in jobs:
      city = job["location"]["name"]
      location = self.geolocator.geocode(city, language="en", timeout=None)
      country = location.address.split(", ")[-1]
      if country in self.eu_countries:
        job["country"] = country
        eu_jobs.append(job)

    return eu_jobs
     

  def get_vacancies(self):
    data = self.scrape()
    tech_jobs = self.filter_tech_jobs(data['jobs'])
    eu_jobs = self.filter_eu_jobs(tech_jobs)
    jobs = self.transform_data(eu_jobs)
    self.update_db(jobs)
    print(f"{self.company} jobs saved")
