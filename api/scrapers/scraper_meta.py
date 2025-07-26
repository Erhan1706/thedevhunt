import requests
from .scraper import Scraper
from jobs.models import Job
from .scraper_registry import register_scraper
from requests.models import Response
from bs4 import BeautifulSoup
import json

@register_scraper("meta")
class MetaScraper(Scraper):
  company = "Meta"

  url = "https://www.metacareers.com/graphql"
  payload = 'av=0&__user=0&__a=1&__req=i&__hs=20156.BP%3ADEFAULT.2.0...0&dpr=1&__ccg=EXCELLENT&__rev=1020727961&__s=3h4cef%3Atrvctf%3A9wj9j4&__hsi=7479798469783935490&__dyn=7xeUmwkHg7ebwKBAg5S1Dxu13wqovzEdEc8uxa1twKzobo1nEhwem0nCq1ewcG0RU2Cwooa81VohwnU14E9k2C0sy0H82NxCawcK1iwmE2ewnE2Lw6OyES4E3PwbS1Lwqo3cwbq0x81nE7u1rw8-1iw&__csr=&__hsdp=&__hblp=&lsd=AVpogfoGfsc&jazoest=21077&__spin_r=1020727961&__spin_b=trunk&__spin_t=1741526291&__jssesw=1&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=CareersJobSearchResultsDataQuery&variables=%7B%22search_input%22%3A%7B%22q%22%3Anull%2C%22divisions%22%3A%5B%5D%2C%22offices%22%3A%5B%22Europe%20%26%20Middle%20East%22%5D%2C%22roles%22%3A%5B%5D%2C%22leadership_levels%22%3A%5B%5D%2C%22saved_jobs%22%3A%5B%5D%2C%22saved_searches%22%3A%5B%5D%2C%22sub_teams%22%3A%5B%5D%2C%22teams%22%3A%5B%22University%20Grad%20-%20Engineering%2C%20Tech%20%26%20Design%22%2C%22Software%20Engineering%22%2C%22Internship%20-%20Engineering%2C%20Tech%20%26%20Design%22%2C%22Data%20%26%20Analytics%22%2C%22Data%20Center%22%2C%22Artificial%20Intelligence%22%2C%22AR%2FVR%22%2C%22Design%20%26%20User%20Experience%22%2C%22Infrastructure%22%2C%22Security%22%5D%2C%22is_leadership%22%3Afalse%2C%22is_remote_only%22%3Afalse%2C%22sort_by_new%22%3Afalse%2C%22results_per_page%22%3Anull%7D%7D&server_timestamps=true&doc_id=9509267205807711'
  headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.metacareers.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.metacareers.com/jobs?offices[0]=Europe%20%26%20Middle%20East&teams[0]=University%20Grad%20-%20Engineering%2C%20Tech%20%26%20Design&teams[1]=Software%20Engineering&teams[2]=Internship%20-%20Engineering%2C%20Tech%20%26%20Design&teams[3]=Data%20%26%20Analytics&teams[4]=Data%20Center&teams[5]=Artificial%20Intelligence&teams[6]=AR%2FVR&teams[7]=Design%20%26%20User%20Experience&teams[8]=Infrastructure&teams[9]=Security',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
    'x-asbd-id': '359341',
    'x-fb-friendly-name': 'CareersJobSearchResultsDataQuery',
    'x-fb-lsd': 'AVpogfoGfsc',
    'Cookie': 'datr=D5XNZ63yXJ5n2nAUlbWvse4N; wd=1016x846'
  }

  def scrape_description(self, job_id) -> tuple | None:
    url = f"https://www.metacareers.com/jobs/{job_id}"
    response: Response = requests.get(url)
    if response.status_code == 200:
      soup: BeautifulSoup = BeautifulSoup(response.text, "lxml")
      description = soup.find("div", class_="_8muv")

      script_tag = soup.find("script", type="application/ld+json")
      if script_tag:
        created_at = json.loads(script_tag.string)["datePosted"] #type: ignore
      else:
        created_at = None
      return str(description), created_at
    else:
      print(f"Request for {url} failed with status code: {response.status_code}")
      return None

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      existing_job = Job.objects.filter(slug=job['id'], company=self.company).first()
      if existing_job:
         description = existing_job.description
         created_at = existing_job.created_at 
      else:
         descriptions = self.scrape_description(job['id'])
         if not descriptions:
            print(f"Failed to fetch description for job {job['id']}")
            continue
         description, created_at = descriptions
      listing = Job(
        title= job['title'],
        slug= job['id'],
        role= self.classify_role_smart(job['teams'][0]),
        company= self.company,
        location= job["locations"],
        link_to_apply= f"https://www.metacareers.com/jobs/{job['id']}",
        employment_type= 'FULL_TIME', 
        remote = False,
        # To reduce number of requests, check if job already exists in db
        description = description,
        created_at = created_at
      )
      result.append(listing)

    return result

  def filter_eu_jobs(self, jobs):
      filtered_jobs = []
      for job in jobs:
          for loc in job['locations']:
              if any(country in loc for country in self.eu_countries):
                  filtered_jobs.append(job)
                  break
      return filtered_jobs

  def get_vacancies(self):
    data = self.scrape("POST")
    eu_jobs= self.filter_eu_jobs(data["data"]["job_search_with_featured_jobs"]["all_jobs"])
    jobs = self.transform_data(eu_jobs)
    self.update_db(jobs)
    print(f'{self.company} jobs saved')
