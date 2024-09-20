from bs4 import BeautifulSoup
import requests
import json
from .scraper import Scraper
from jobs.models import Job
from time import sleep
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import time
from playwright.async_api import async_playwright
import asyncio

class ThalesScraper(Scraper):
  url = "https://careers.thalesgroup.com/widgets"
  headers = {
  'Content-Type': 'application/json',
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
  
  async def description_to_html(self, url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector('div.jd-info', timeout=20000)
        description = await page.query_selector('div.jd-info')
        if description:
            html = await description.inner_html()
            await browser.close()
            return html
        else:
            print(f"Request for {url} failed")
            await browser.close()
            return None

  async def transform_data(self, jobs):
    result = []
    for job in jobs:
      listing = Job(
        title= job['title'],
        slug= job['reqId'],
        role= job['category'],
        technologies= job['ml_skills'],
        company= "Thales",
        location= [f"{job['city']}, {job['country']}"],
        link_to_apply= f"https://careers.thalesgroup.com/global/en/job/{job['reqId']}",
        created_at= job['dateCreated'],
        employment_type= 'FULL_TIME' if job['type'] == 'Full time' else 'PART_TIME',
        remote = False
      )
      description = await self.description_to_html(listing.link_to_apply)
      if not description: continue
      listing.description = description
      result.append(listing)

    return result

  def get_vacancies(self):
    _start = time()
    data = self.scrape()
    jobs = data['refineSearch']['data']['jobs']
    jobs = jobs
    result = asyncio.run(self.transform_data(jobs))
    self.update_db(result)
    print('Thales jobs saved')
    print(f"finished in: {time() - _start:.2f} seconds")

