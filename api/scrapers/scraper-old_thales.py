from bs4 import BeautifulSoup
import requests
import json
from .scraper import Scraper
from jobs.models import Job
from time import time
from playwright.async_api import async_playwright
import asyncio
import random
from .scraper_registry import register_scraper

@register_scraper("thales")
class ThalesScraper(Scraper):
  url = "https://careers.thalesgroup.com/widgets"
  headers = {
  "Content-Type": 'application/json',
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Accept-Language": "en-US,en;q=0.9"
  }

  payload = json.dumps({
    "lang": "en_global",
    "deviceType": "desktop",
    "country": "global",
    "pageName": "search-results",
    "ddoKey": "refineSearch",
    "sortBy": "",
    "subsearch": "",
    "from": 0,
    "jobs": True,
    "counts": True,
    "all_fields": [
      "category",
      "country",
      "state",
      "city",
      "type",
      "workerSubType",
      "workLocation"
    ],
    "size": 1000,
    "clearAll": False,
    "jdsource": "facets",
    "isSliderEnable": False,
    "pageId": "page18",
    "siteType": "external",
    "keywords": "",
    "global": True,
    "selected_fields": {
    "country": [
        "Belgium",
        "Denmark",
        "France",
        "Greece",
        "Italy",
        "Netherlands",
        "Norway",
        "Poland",
        "Portugal",
        "Switzerland",
        "Spain",
        "Romania",
        "Luxembourg",
        "Czechia",
        "United Kingdom",
        "Germany",
        "Austria",
        "Sweden",
        "Finland",
        "Hungary",
        "Ireland",
        "Slovakia",
        "Bulgaria",
        "Croatia",
        "Estonia",
        "Latvia",
        "Lithuania",
        "Slovenia",
        "Cyprus",
        "Iceland",
        "Monaco",
        "Andorra",
        "Albania",
        "Bosnia and Herzegovina",
        "Montenegro",
        "North Macedonia",
        "Serbia",
        "Turkey",
        "Ukraine",
        "Belarus",
        "Moldova",
      ],
      "category": [
        "Information Systems - Information Technology",
        "Software",
        "System",
        "Hardware"
      ]
    },
    "locationData": {}
  })

  def scrape_custom(self):
    response = requests.request("POST", self.url, headers=self.headers, data=self.payload)
    if response.status_code == 200:
      try:
        data = response.json() 
        return data
      except ValueError:
        print("Response content for Thales is not valid JSON")
        raise Exception("Invalid JSON response from Thales API")
    else:
      raise Exception(f"Request for {self.url} failed with status code: {response.status_code}")
  
  async def fetch_descriptions(self, job_links):
    """Launch a browser instance and fetch job descriptions concurrently."""
    async with async_playwright() as p:
      browser = await p.chromium.launch()
      page = await browser.new_page()

      async def fetch_description(url):
        await asyncio.sleep(random.uniform(0, 15)) 
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector('div.jd-info', timeout=2000)
        description = await page.query_selector('div.jd-info')
        return await description.inner_html() if description else None

      tasks = [fetch_description(link) for link in job_links]
      descriptions = await asyncio.gather(*tasks, return_exceptions=True)

      await browser.close()
      return descriptions
    
  async def transform_data_async(self, jobs):
    job_listings = [
        Job(
            title=job['title'],
            slug=job['reqId'],
            role=job['category'],
            technologies=job.get('ml_skills', []),
            company="Thales",
            location=[f"{job['city']}, {job['country']}"],
            link_to_apply=f"https://careers.thalesgroup.com/global/en/job/{job['reqId']}",
            created_at=job['dateCreated'],
            employment_type='FULL_TIME' if job['type'] == 'Full time' else 'PART_TIME',
            remote=False
        )
        for job in jobs
    ]

    job_links = [listing.link_to_apply for listing in job_listings]
    descriptions = await self.fetch_descriptions(job_links)

    for listing, description in zip(job_listings, descriptions):
        if description:
            listing.description = description

    return job_listings

  def get_vacancies(self):
    _start = time()
    data = self.scrape_custom()
    jobs = data['refineSearch']['data']['jobs']
    result = asyncio.run(self.transform_data_async(jobs))
    self.update_db(result)
    print('Thales jobs saved')
    print(f"finished in: {time() - _start:.2f} seconds")

