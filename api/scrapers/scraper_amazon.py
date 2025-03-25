import requests
from .scraper import Scraper
from jobs.models import Job
import time
from .scraper_registry import register_scraper
from datetime import datetime
from time import sleep

@register_scraper("amazon")
class AmazonScraper(Scraper):
  company = "Amazon"

  base_url = "https://www.amazon.jobs/en/search.json?category%5B%5D=operations-it-support-engineering&category%5B%5D=software-development&category%5B%5D=systems-quality-security-engineering&category%5B%5D=project-program-product-management-technical&category%5B%5D=project-program-product-management-non-tech&category%5B%5D=solutions-architect&category%5B%5D=machine-learning-science&category%5B%5D=hardware-development&category%5B%5D=data-science&radius=24km&facets%5B%5D=normalized_country_code&facets%5B%5D=normalized_state_name&facets%5B%5D=normalized_city_name&facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location&facets%5B%5D=job_function_id&facets%5B%5D=is_manager&facets%5B%5D=is_intern&result_limit=100&sort=relevant&latitude=&longitude=&loc_group_id=&base_query=&city=&region=&county=&query_options="
  country_codes = {"NLD": "Netherlands", "DEU": "Germany", "EST": "Estonia", "IRL": "Ireland" ,
                   "GBR": "United Kingdom", "ESP": "Spain", "ITA": "Italy", "BEL": "Belgium",
                   "FRA": "France", "LUX": "Luxembourg", "POL": "Poland", "ROU": "Romania",
                   "SWE": "Sweden", "FIN": "Finland",} 
  payload = {}
  headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
  }

  def scrape(self, url):
    """ Scrape all jobs from Amazon API. Navigate through the paginated results """
    offset = 0
    all_jobs = []
    response = requests.request("GET", f"{url}&offset={offset}", headers=self.headers, data=self.payload)
    total_hits = response.json()["hits"]    

    while total_hits > 0:
      response = requests.request("GET", f"{url}&offset={offset}", headers=self.headers, data=self.payload)
      if response.status_code != 200:
        raise Exception(f"Request for {url} failed with status code: {response.status_code}")
      data = response.json()
      all_jobs += data['jobs']
      offset += 100
      total_hits -= 100
      sleep(0.5)
    
    return all_jobs
  
  def transform_data(self, jobs):
    result = []
    for job in jobs:
      listing = Job(
        title= job['title'],
        slug= job['id'],
        role= job['job_category'],
        company= self.company,
        location= [f"{job['city']}, {self.country_codes[job['country_code']]}"],
        link_to_apply= f"https://amazon.jobs/{job['job_path']}",
        created_at= datetime.strptime(job['posted_date'], "%B %d, %Y").isoformat() + "Z", # Convert dates like "June 1, 2021" to iso format
        employment_type= 'FULL_TIME' if job['job_schedule_type'] == 'full-time' else 'INTERNSHIP',
        remote = False,
        description = f"<br>{job['description']}" 
      )
      result.append(listing)

    return result

  def get_vacancies(self):
    all_jobs = []
    for code in self.country_codes.keys():
      url = f"{self.base_url}&loc_query={self.country_codes[code]}&country={code}"
      data = self.scrape(url)
      jobs = self.transform_data(data)
      all_jobs += jobs 
      sleep(0.5)
    self.update_db(all_jobs)
    print(f'{self.company} jobs saved')
