from bs4 import BeautifulSoup
import requests
import json
from .scraper import Scraper
from jobs.models import Job
from requests_html import HTMLSession
from time import sleep

class UberScraper(Scraper):
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
        "Engineering"
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
    
  def description_to_html(self, url):
    sleep(1)    
    session = HTMLSession()
    response = session.get(url, headers=self.headers_description)

    try: 
      response.html.render(timeout=20)
      description = response.html.find('div.css-cvJeNJ', first=True)
      session.close()
      print('Success')
      return description.html
    except Exception as e:
      print(f"Error rendering page: {url}")
      session.close()
      return None

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
        description = job['description']
      )
      description = self.description_to_html(listing.link_to_apply)
      if not description: continue
      listing.description = description
      result.append(listing)

    return result


  def get_vacancies(self):
    data = self.scrape()
    jobs = self.transform_data(data['data']['results'])
    for job in jobs:
      job.save()
    print('Uber jobs saved')