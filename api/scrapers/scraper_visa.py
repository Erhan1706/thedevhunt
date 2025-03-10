import json
from .scraper import Scraper
from jobs.models import Job
from .scraper_registry import register_scraper

@register_scraper("optiver")
class VisaScraper(Scraper):

  url = "https://search.visa.com/CAREERS/careers/jobs?q="
  company = "VISA"

  payload = json.dumps({
    "filters": [
      {
        "department": [
          "Cyber Security",
          "Data Architect/Engineering/Science",
          "Data Science/Data Engineering",
          "Information Technology",
          "Software Development/Engineering",
          "Software Quality Assurance and Testing",
          "UI/UX Design & Development"
        ]
      }
    ],
    "city": [
      "Vienna",
      "Sofia",
      "Strovolos",
      "Prague",
      "Praha",
      "Copenhagen",
      "Paris",
      "Berlin",
      "Frankfurt",
      "Munich",
      "Athens",
      "Budapest",
      "Milano",
      "Riga",
      "Swatar",
      "Amsterdam",
      "Oslo",
      "Poznań",
      "Warsaw",
      "Lisbon",
      "Bucharest",
      "Belgrade",
      "Madrid",
      "Zurich",
      "Zürich",
      "Kiev",
      "Kyiv",
      "Belfast",
      "Cardiff",
      "London",
      "Reading",
      "Helsinki"
    ],
    "from": 0,
    "size": 10
  })
  headers = {
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en-GB,en;q=0.8',
      'Content-Type': 'application/json',
      'cache-control': 'no-cache',
      'pragma': 'no-cache',
      'priority': 'u=1, i',
      'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'sec-gpc': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
  }

  def transform_data(self, jobs):
    result = []
    for job in jobs:
        listing = Job(
            role = job["department"],
            company = "VISA",
            title = job["jobTitle"],
            location= [f"{job['city']}, {job['country']}"],
            slug = job["postingId"],
            link_to_apply = job["applyUrl"],
            remote = False,
            created_at= job['createdOn'],
            employment_type = 'FULL_TIME' if job["typeOfEmployment"] == "Full-time" else 'PART_TIME',
            description = job["jobDescription"]
        )
        result.append(listing)
    return result

  def get_vacancies(self):
    data = self.scrape(method="POST")
    jobs = self.transform_data(data['jobDetails'])
    self.update_db(jobs)
    print('VISA jobs saved')