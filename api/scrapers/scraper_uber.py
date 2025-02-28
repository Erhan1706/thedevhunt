import requests
import json
from .scraper import Scraper
from jobs.models import Job
import markdown2

class UberScraper(Scraper):
  company = "Uber"
  url = "https://www.uber.com/api/loadSearchJobsResults?localeCode=en"
  payload = json.dumps({
    "params": {
      "location": [
        {
          "country": "NOR",
          "city": "Oslo"
        },
        {
          "country": "NLD",
          "city": "Amsterdam"
        },
        {
          "country": "DEU",
          "city": "Berlin"
        },
        {
          "country": "DEU",
          "city": "Hamburg"
        },
        {
          "country": "DEU",
          "city": "Munich"
        },
        {
          "country": "DEU",
          "city": "Dusseldorf"
        },
        {
          "country": "GBR",
          "city": "London"
        },
        {
          "country": "POL",
          "city": "Krakow"
        },
        {
          "country": "GBR",
          "city": "Birmingham"
        },
        {
          "country": "GBR",
          "city": "Southampton"
        },
        {
          "country": "GBR",
          "city": "Belfast"
        },
        {
          "country": "PRT",
          "city": "Lisbon"
        },
        {
          "country": "POL",
          "city": "Warsaw"
        },
        {
          "country": "GBR",
          "city": "Leeds"
        },
        {
          "country": "FRA",
          "city": "Lyon"
        },
        {
          "country": "CHE",
          "city": "Zurich"
        },
        {
          "country": "GBR",
          "city": "Newcastle Upon Tyne"
        },
        {
          "country": "DNK",
          "city": "Aarhus"
        },
        {
          "country": "TUR",
          "city": "Istanbul"
        },
        {
          "country": "IRL",
          "city": "Dublin"
        },
        {
          "country": "IRL",
          "city": "Limerick"
        },
        {
          "country": "ESP",
          "city": "Madrid"
        },
        {
          "country": "ESP",
          "city": "Barcelona"
        },
        {
          "country": "FRA",
          "city": "Paris"
        },
        {
          "country": "FRA",
          "city": "Aubervilliers"
        },
        {
          "country": "BEL",
          "city": "Brussels"
        },
        {
          "country": "SWE",
          "city": "Stockholm"
        }
      ],
      "department": [
        "Data Science",
        "Engineering",
        "Product",
        "Design",
      ],
      "team": [],
      "programAndPlatform": [],
      "lineOfBusinessName": []
    },
    "page": 0,
    "limit": 1000
  })

  headers = {
      'accept': '*/*',
      'accept-language': 'en-GB,en;q=0.7',
      'pragma': 'no-cache',
      'priority': 'u=1, i',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'sec-gpc': '1',
      'x-csrf-token': 'x',
      'x-uber-sites-page-edge-cache-enabled': 'true',
      'origin': 'https://www.uber.com',
      'Content-Type': 'application/json',
  }

  headers_description = {
    'accept-language': 'en-GB,en;q=0.7',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'x-uber-sites-page-edge-cache-enabled': 'true',
    'origin': 'https://www.uber.com',
    'Content-Type': 'application/json',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  }

  def scrape(self):
    response = requests.request("POST", self.url, headers=self.headers, data=self.payload)
    if response.status_code == 200:
      try:
        data = response.json() 
        return data
      except ValueError:
        print("Response content for Booking.com is not valid JSON")
    else:
      raise Exception(f"Request for {self.url} failed with status code: {response.status_code}")
    
  def transform_data(self, jobs):
    result = []
    for job in jobs:
      locations = []
      for loc in job['allLocations']:
        locations.append(f"{loc['city']}, {loc['countryName']}")
      listing = Job(
        title= job['title'],
        slug= job['id'],
        role= job['department'],
        company= "Uber",
        location= locations,
        link_to_apply= f"https://www.uber.com/global/en/careers/list/{job['id']}",
        created_at= job['creationDate'],
        employment_type= 'FULL_TIME' if job['type'] == 'Full-Time' else 'PART_TIME',
        remote = False,
        description = markdown2.markdown(job['description'])
      )
      result.append(listing)

    return result


  def get_vacancies(self):
    data = self.scrape()
    jobs = self.transform_data(data['data']['results'])
    self.update_db(jobs)
    print(f'{self.company} jobs saved')
