import requests
from .scraper import Scraper
from jobs.models import Job
from .scraper_registry import register_scraper

@register_scraper("optiver")
class OptiverScraper(Scraper):

  url_amsterdam = "https://optiver.com/wp-admin/admin-ajax.php?action=get_posts&numberposts=100&paged=1&viewmode=list&post_type=job&level=&department=technology&office=amsterdam&search="
  url_london = "https://optiver.com/wp-admin/admin-ajax.php?action=get_posts&numberposts=100&paged=1&viewmode=list&post_type=job&level=&department=technology&office=london&search="

  company = "Optiver"
  headers = {}
  payload = {}

  def scrape(self, city='') -> dict: #type: ignore
    """ Currently Optiver only has two offices in Europe """
    response = None
    if city == 'amsterdam':
      response = requests.request("POST", self.url_amsterdam)
    elif city == 'london':
      response = requests.request("POST", self.url_london)
    if response is not None and response.status_code == 200:
      try:
        data = response.json() 
        return data
      except ValueError:
        print("Response content for Optiver is not valid JSON")
    elif response is not None:
      raise Exception(f"Request for Optiver failed with status code: {response.status_code}")
    else:
      raise Exception("No response received for Optiver scrape; invalid city parameter?")
  
  def transform_data(self, jobs, city="") -> list:
    result = []
    for job in jobs:
        listing = Job(
            role = self.classify_role_smart(job["post_title"]),
            company = "Optiver",
            title = job["post_title"],
            location= ["Amsterdam, Netherlands"] if city == 'amsterdam' else ["London, United Kingdom"],
            slug = job["ID"],
            link_to_apply = f"https://optiver.com/working-at-optiver/career-opportunities/{job['post_name']}",
            remote = False,
            created_at= job['post_date'],
            employment_type = 'FULL_TIME' if not "intern" in job["post_title"].lower() else 'INTERNSHIP',
            description = job["post_content"]
        )
        result.append(listing)
    return result
  
  def get_vacancies(self):
    data_amsterdam = self.scrape(city='amsterdam')
    data_london = self.scrape(city='london')
    jobs_ams = self.transform_data(data_amsterdam['result']['result'], city='amsterdam')
    jobs_lon = self.transform_data(data_london['result']['result'], city='london')
    jobs = jobs_ams + jobs_lon
    self.update_db(jobs)
    print("Optiver jobs saved")
