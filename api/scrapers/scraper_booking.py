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
        with open('response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2) 
      except ValueError:
        print("Response content for Booking.com is not valid JSON")
    else:
      print(f"Request for {self.url} failed with status code: {response.status_code}")


  def description_to_html(self, url):
    def find_description_script(tag):
      return (tag.name == "script" and 
              "window.jobDescriptionConfig = " in tag.string if tag.string else False)
    
    sleep(0.5) # To avoid getting blocked by the server
    try:
        response = requests.get(url)
    except ChunkedEncodingError as ex:
        print(f"Invalid chunk encoding {str(ex)}")

    if response.status_code == 200:
      soup: BeautifulSoup = BeautifulSoup(response.content, "lxml")
      script_tag = soup.find(find_description_script)
      description_json = script_tag.text.split("window.jobDescriptionConfig = ")[1]
      description = json.loads(description_json[:-2])
      return description['job']['description']
    else:
      print(f"Request for {self.url} failed with status code: {response.status_code}")
    
  
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
        employment_type= 'FULL-TIME',
        remote = True if 'remote' in job['location_name'].lower() or 'remote' in job['street_address'].lower() else False
      )
      listing.description = self.description_to_html(listing.link_to_apply)
      result.append(listing)
      break 

    return result

  def filter_tech_jobs(self, jobs):
    tech_keywords = {"data", "engineering", "it", "security"}
    job_list = jobs['jobs']
    return [job for job in job_list if any(keyword in job['data']['category'][0].lower() for keyword in tech_keywords)]
  
  def get_vacancies(self):
    #jobs = self.scrape()
    with open('./api/scrapers/response.json', 'r', encoding='utf-8') as f:
      data = json.load(f)
      jobs = self.filter_tech_jobs(data)
      jobs = [job['data'] for job in jobs]
      filtered_jobs = self.filter_eu_jobs(jobs, location_key='country')
      jobs = self.transform_data(filtered_jobs)
      #for job in jobs:
        #job.save()