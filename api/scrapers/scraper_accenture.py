from .scraper import Scraper
from jobs.models import Job
from datetime import datetime, timezone


class AccentureScraper(Scraper):
  url = "https://www.accenture.com/api/accenture/jobsearch/result"

  payload = {
    'startIndex': '0',
    'maxResultSize': '1000',
    'jobKeyword': '',
    'jobLanguage': 'en',
    'countrySite': 'nl-en',
    'jobFilters': '[{"fieldName":"businessArea","items":["technology"]}]',
    'aggregations': '[{"fieldName":"location"},{"fieldName":"postedDate"},{"fieldName":"jobTypeDescription"},{"fieldName":"workforceEntity"},{"fieldName":"businessArea"},{"fieldName":"skill"},{"fieldName":"travelPercentage"},{"fieldName":"yearsOfExperience"},{"fieldName":"specialization"},{"fieldName":"employeeType"},{"fieldName":"remoteType"}]',
    'jobCountry': 'Netherlands',
    'sortBy': '1',
    'componentId': 'careerjobsearchresults-79f061dad5'
  }

  headers = {
    'Accept-Language': 'en-GB,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Origin': 'https://www.accenture.com',
    'Pragma': 'no-cache',
    'Priority': 'u=1, i',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
  }

  company = "Accenture"

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      listing = Job(
        title= job['title'],
        slug= job['jobId'],
        role= job['skill'],
        company= "Accenture",
        location= [f"{job['jobCityState'][0]}, {job['country']}"],
        link_to_apply= job['jobDetailUrl'],
        employment_type= 'FULL_TIME' if job['employeeType'] == 'Full-time' else 'INTERNSHIP',
        remote = False,
        description = job['jobDescription'],
        created_at= datetime.fromtimestamp(job['postedDate'] / 1000, timezone.utc)
      )
      result.append(listing)

    return result

  def filter_tech_jobs(self, jobs):
    tech_keywords = {"software", "data"}
    return [job for job in jobs if any(keyword in job['skill'].lower() for keyword in tech_keywords)]
  
  def get_vacancies(self):
    data = self.scrape(method="POST")
    jobs = self.filter_tech_jobs(data['data'])
    jobs = self.transform_data(jobs)
    self.update_db(jobs)
    print('Accenture jobs saved')
