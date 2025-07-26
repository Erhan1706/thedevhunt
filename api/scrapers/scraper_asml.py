from .scraper import Scraper
from jobs.models import Job
import json
from .scraper_registry import register_scraper
import requests

@register_scraper("asml")
class ASMLScraper(Scraper):
  url = "https://discover-euc1.sitecorecloud.io/discover/v2/126200477"
  company = "ASML"


  payload = json.dumps({
    "context": {
      "page": {
        "uri": "https://www.asml.com/en/careers/find-your-job?icmp=careers-home-header-link&job_country=Netherlands&job_educational_backgrounds=Computer+Science&job_type=Fix"
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
                  "name": "job_country",
                  "values": [
                    "Netherlands"
                  ],
                  "type": "anyOf"
                },
                {
                  "name": "job_type",
                  "values": [
                    "Fix"
                  ],
                  "type": "anyOf"
                },
                {
                  "name": "job_educational_backgrounds",
                  "values": [
                    "Computer Science",
                    "Data Science"
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

  payload2 = json.dumps({
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

  def scrape_custom(self, payload, method="GET") -> dict:
    response = requests.request(method, self.url, headers=self.headers, data=payload, verify=False)
    if response.status_code == 200:
      try:
        data = response.json() 
        return data
      except ValueError:
        print(f"Response content for {self.company} is not valid JSON")
        raise ValueError(f"Response content for {self.company} is not valid JSON")
    else:
      raise Exception(f"Request for {self.url} failed with status code: {response.status_code}")

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      # For some reason data does not always come in a consistent format
      if job['job_technical_fields'] and len(job['job_technical_fields']) > 0:
        role = job['job_technical_fields'][0]
      elif job['job_teams'] and len(job['job_teams']) > 0:
        role = job['job_teams'][0]
      else: role = None

      listing = Job(
        title= job['name'],
        slug= job['id'],
        role= self.classify_role_smart(role) if role else None,
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
    jobs1 = self.scrape_custom(payload=self.payload, method="POST")
    jobs2 = self.scrape_custom(payload=self.payload2, method="POST") # Second payload for different job types
    all_jobs = jobs1['widgets'][0]['content'] + jobs2['widgets'][0]['content']
    eu_jobs = self.filter_eu_jobs(all_jobs)
    jobs = self.transform_data(eu_jobs)
    self.update_db(jobs)
    print(f"{self.company} jobs saved")
