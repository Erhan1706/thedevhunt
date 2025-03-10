import requests
from .scraper import Scraper
from jobs.models import Job
import time
import re
from .scraper_registry import register_scraper

@register_scraper("microsoft")
class MicrosoftScraper(Scraper):
  company = "Microsoft"

  relevant_countries = ["Netherlands", "United%20Kingdom", "Germany", "France", "Austria", "Ireland", "Czech%20Republic", 
                        "Denmark", "Belgium", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden", "Estonia", "Finland", 
                        "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Türkiye","Luxembourg", "Serbia", "Slovakia", "Slovenia"]
  

  url = "https://gcsservices.careers.microsoft.com/search/api/v1/search?"
  url_filters = "&p=Data%20Center&p=Software%20Engineering&p=Hardware%20Engineering&p=Technical%20Support&l=en_us&pgSz=20&o=Relevance&flt=true"

  payload = {}
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer undefined',
    'cache-control': 'no-cache',
    'origin': 'https://jobs.careers.microsoft.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://jobs.careers.microsoft.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-correlationid': 'eaf31e1c-8eed-207b-faea-37e23c6b84d7',
    'x-subcorrelationid': '3189c374-6e6a-08f2-7223-4267c0a7b1a7'
  }

  def scrape(self):
    """ Try to minize the amount of data scraped by filtering only relevant countries. Microsoft API limits to max 8 countries """
    data = []
    
    for i in range(0, len(self.relevant_countries), 8):
        chunk = self.relevant_countries[i:i + 8]
        
        url_to_scrape = self.url
        for country in chunk:
            url_to_scrape += f"&lc={country}"
        url_to_scrape += self.url_filters
        
        data += self.scrape_all_jobs(url_to_scrape)        
        time.sleep(1)
    
    return data
    

  def scrape_all_jobs(self, url):
    """ Scrape all jobs from Microsoft API. Navigate through the paginated results """
    i = 1
    all_jobs = []
    while True:
      response = requests.request("GET", f"{url}&pg={i}", headers=self.headers, data=self.payload)
      if response.status_code != 200:
        raise Exception(f"Request for {url} failed with status code: {response.status_code}")
      data = response.json()
      jobs = data['operationResult']['result']['jobs']
      if len(jobs) == 0:
        break
      all_jobs += jobs
      i += 1
      time.sleep(0.5)
    return all_jobs


  def transform_data(self, jobs):
    result = []
    for job in jobs:
      locations = []
      for loc in job['properties']['locations']:
        loc_str = loc.split(', ')
        locations.append(f"{loc_str[1]}, {loc_str[2]}") if loc_str[1] != 'Multiple Locations' else locations.append(loc_str[2])

      listing = Job(
        title= job['title'],
        slug= job['jobId'],
        role= job['properties']['profession'],
        company= self.company,
        location= locations,
        link_to_apply= f"https://jobs.careers.microsoft.com/global/en/job/{job['jobId']}",
        created_at= job['postingDate'],
        employment_type= 'FULL_TIME' if job['properties']['employmentType'] == 'Full-Time' else 'INTERNSHIP',
        remote = False if job['properties']['workSiteFlexibility'] == 'Microsoft on-site only' else True,
        description =  re.sub(r'style="[^"]*"', '', job['properties']['description'])
      )
      result.append(listing)

    return result


  def get_vacancies(self):
    data = self.scrape()
    jobs = self.transform_data(data)
    self.update_db(jobs)
    print(f'{self.company} jobs saved')
