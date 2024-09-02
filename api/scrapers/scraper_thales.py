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
  
  def description_to_html(self, url):
    options = Options()
    options.add_argument('-headless')
    options.add_argument('-no-sandbox')
    options.add_argument('-disable-dev-shm-usage')
    
    driver = webdriver.Firefox(options=options)
    try:
        driver.get(url)
        # Wait for the specific element to be present
        wait = WebDriverWait(driver, 20)
        description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jd-info')))
        
        # Print page source for debugging
        print(f"Page source for {url}:")

        return description.get_attribute('outerHTML')
    except Exception as e:
        print(f"Error while fetching description for {url}: {e}")
        return None
    finally:
        driver.quit()

  def transform_data(self, jobs):
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
      description = self.description_to_html(listing.link_to_apply)
      if not description: continue
      listing.description = description
      result.append(listing)

    return result

  def get_vacancies(self):
    data = self.scrape()
    jobs = data['refineSearch']['data']['jobs']
    result = self.transform_data(jobs)
    self.update_db(result)
    print('Thales jobs saved')
