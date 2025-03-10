from .scraper import Scraper
from jobs.models import Job
import json
from .scraper_registry import register_scraper

@register_scraper("asml")
class ASMLScraper(Scraper):
  url = "https://discover-euc1.sitecorecloud.io/discover/v2/126200477"
  company = "ASML"


  payload = json.dumps({
    "context": {
      "page": {
        "uri": "https://www.asml.com/en/careers/find-your-job?icmp=careers-home-header-link&job_technical_fields=IT%7CSoftware%7CSystem+Integration+and+Testing&job_type=Fix"
      },
      "locale": {
        "country": "us",
        "language": "en"
      }
    },
    "widget": {
      "items": [
        {
          "entity": "content",
          "rfk_id": "asml_job_search",
          "search": {
            "limit": 100,
            "offset": 0,
            "content": {},
            "filter": {
              "type": "and",
              "filters": [
                {
                  "name": "job_type",
                  "values": [
                    "Fix"
                  ],
                  "type": "anyOf"
                },
                {
                  "name": "job_technical_fields",
                  "values": [
                    "IT",
                    "Software",
                    "System Integration and Testing"
                  ],
                  "type": "anyOf"
                }
              ]
            }
          }
        }
      ]
    }
  })

  headers = {
    'accept': 'application/json',
    'authorization': '01-967712c8-5a349c1760436ea6dccfd7bb02bfbe4dc2ccc36c',
    'accept-language': 'en-US,en;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.asml.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.asml.com/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
  }

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      listing = Job(
        title= job['name'],
        slug= job['id'],
        role= job['job_technical_fields'][0] if len(job['job_technical_fields']) > 0 else None,
        company= self.company,
        location= [f"{job['job_city']}, {job['job_country']}"],
        link_to_apply= job['url'],
        employment_type= 'FULL_TIME',
        remote = False,
        description = job['description'],
        created_at= job['job_date_posted']
      )
      result.append(listing)

    return result
  
  def filter_eu_jobs(self, jobs):
    return [job for job in jobs if any(country in job['job_country'] for country in self.eu_countries)]

  def get_vacancies(self):
    jobs = self.scrape(method="POST")
    eu_jobs = self.filter_eu_jobs(jobs['widgets'][0]['content'])
    jobs = self.transform_data(eu_jobs)
    self.update_db(jobs)
    print(f"{self.company} jobs saved")
