from bs4 import BeautifulSoup
import requests
import json
from .scraper import Scraper
from jobs.models import Job
from time import sleep
from requests.exceptions import ChunkedEncodingError


class BookingScraper(Scraper):
  url = "https://jobs.booking.com/api/jobs?location=Europe&stretch=25&stretchUnit=MILES&page=1&sortBy=relevance&descending=false&internal=false&tags1=Booking.com%20Company%20Hierarchy%7CTransport%20Company%20Hierarchy&limit=100"
  headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-GB,en;q=0.8',
      'cache-control': 'no-cache',
      'pragma': 'no-cache',
      'priority': 'u=1, i',
      'referer': 'https://jobs.booking.com/booking/jobs?location=Europe&stretch=25&stretchUnit=MILES&page=1',
      'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'sec-gpc': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
  }
    
  def scrape(self):
    response = requests.request("GET", self.url, headers=self.headers)
    if response.status_code == 200:
      try:
        data = response.json() 
        return data
      except ValueError:
        print("Response content for Booking.com is not valid JSON")
    else:
      raise Exception(f"Request for {self.url} failed with status code: {response.status_code}")


  def description_to_html(self, url):
    def find_description_script(tag):
      return (tag.name == "script" and 
              "window.jobDescriptionConfig = " in tag.string if tag.string else False)
    
    response = None
    for attempt in range(5):
      try:
        response = requests.get(url)
      except ChunkedEncodingError as ex:
        print(f"Invalid chunk encoding on: {url}")
        sleep(2**attempt * 0.4)

    if response and response.status_code == 200:
      soup: BeautifulSoup = BeautifulSoup(response.content, "lxml")
      script_tag = soup.find(find_description_script)
      description_json = script_tag.text.split("window.jobDescriptionConfig = ")[1]
      description = json.loads(description_json[:-2])
      return description['job']['description']
    else:
      print(f"Request for {url} failed")
      return None 
    
  
  def transform_data(self, jobs):
    result = []
    for job in jobs:
      listing = Job(
        title= job['title'],
        slug= job['slug'],
        role= job['category'][0],
        company= "Booking.com",
        location= [job['full_location']],
        link_to_apply= f"https://jobs.booking.com/booking/jobs/{job['slug']}?lang=en-us",
        created_at= job['create_date'],
        employment_type= 'FULL_TIME',
        remote = True if 'remote' in job['location_name'].lower() or 'remote' in job['street_address'].lower() else False
      )
      #description = self.description_to_html(listing.link_to_apply)
      #if not description: continue
      #listing.description = description
      result.append(listing)

    return result

  def filter_tech_jobs(self, jobs):
    tech_keywords = {"data", "engineering", "it", "security"}
    job_list = jobs['jobs']
    return [job for job in job_list if any(keyword in job['data']['category'][0].lower() for keyword in tech_keywords)]
  
  def filter_eu_jobs(self, jobs, location_key):
    eu_countries = ["Netherlands", "United Kingdom", "Germany", "France", "Austria", "Ireland", "Czech Republic", 
                    "Denmark", "Belgium", "Croatia", "Portugal", "Spain", "Romania", "Poland", "Norway", "Sweden",
                    "Cyprus", "Estonia", "Finland", "Greece", "Hungary", "Italy", "Bulgaria", "Switzerland", "Turkey",
                    "Iceland", "Latvia", "Lithuania", "Luxembourg", "Malta", "Russia", "Serbia", "Slovakia", 
                    "Ukraine", "Slovenia", "Belarus", "Bosnia and Herzegovina", "Moldova", "Montenegro",
                    "San Marino", "Vatican City", "Liechtenstein", "Albania","Kosovo", "Monaco", "North Macedonia", "Andorra"]
    
    return [job for job in jobs if any(country in job[location_key] for country in eu_countries)]
  
  def get_vacancies(self):
    data = self.scrape()
    jobs = self.filter_tech_jobs(data)
    jobs = [job['data'] for job in jobs]
    filtered_jobs = self.filter_eu_jobs(jobs, 'country')
    jobs = self.transform_data(filtered_jobs)
    self.update_db(jobs)
    print('Booking.com jobs saved')
