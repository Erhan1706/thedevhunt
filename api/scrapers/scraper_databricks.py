from .scraper import Scraper
from jobs.models import Job
from geopy.geocoders import Nominatim
import html


class DatabricksScaper(Scraper):

  url = "https://www.databricks.com/careers-assets/page-data/company/careers/open-positions/page-data.json"

  headers = {}
  payload = {}

  company = "Databricks"

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      listing = Job(
        title= job['title'],
        slug= job['id'],
        role= job['metadata'][0]['value'][0] if len(job['metadata'][0]['value']) > 0 else None,
        company= self.company,
        location= [f"{job['location']['name']}"],
        link_to_apply= job['absolute_url'],
        employment_type= 'FULL_TIME',
        remote = False,
        description = html.unescape(job['content']),
        created_at= job['updated_at']
      )
      result.append(listing)

    return result
  
  def filter_tech_jobs(self, jobs):
    revelevant_databricks_departments = {"Engineering", "Field Engineering", "IT", "Mosaic AI", "Security", "Product"}
    tech_jobs = []
    for job in jobs:
      department = job['metadata'][0]['value']
      if not department or len(department) == 0: continue
      if department[0] in revelevant_databricks_departments:
        tech_jobs.append(job)
    return tech_jobs

  def filter_eu_jobs(self, jobs):
    return [job for job in jobs if any(country in job['location']['name'] for country in self.eu_countries)]

  def get_vacancies(self):
    data = self.scrape()
    tech_jobs = self.filter_tech_jobs(data['result']['pageContext']['data']['allGreenhouseJob']['nodes'])
    eu_jobs = self.filter_eu_jobs(tech_jobs)
    jobs = self.transform_data(eu_jobs)
    self.update_db(jobs)
    print(f"{self.company} jobs saved")