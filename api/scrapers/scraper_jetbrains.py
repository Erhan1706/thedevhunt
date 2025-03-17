from bs4 import BeautifulSoup
import requests
from requests.models import Response
import json
from .scraper import Scraper
from jobs.models import Job
from .scraper_registry import register_scraper

@register_scraper("jetbrains")
class JetbrainsScraper(Scraper):

    URL = "https://www.jetbrains.com/careers/jobs/"
    
    def scrape(self):
        page_source: Response =  requests.get(self.URL)
        if page_source.status_code != 200:
            raise Exception(f"Request for {self.URL} failed with status code: {page_source.status_code}")

        soup: BeautifulSoup = BeautifulSoup(page_source.text, "lxml")

        def find_vacancies_script(tag):
            return (tag.name == "script" and 
                    "var VACANCIES =" in tag.string if tag.string else False)

        vacancies_script = soup.find(find_vacancies_script)
        json_vacancies = json.loads(vacancies_script.contents[0].split("var VACANCIES = ")[1].strip())
        return json_vacancies
    
    def transform_data(self, jobs) -> list:
        result = []
        for job in jobs:
            listing = Job(
                role = job["role"][0],
                company = "Jetbrains",
                title = job["title"],
                location = job["location"],
                slug = job["slug"],
                link_to_apply = f"https://www.jetbrains.com/careers/jobs/{job['slug']}/",
                remote = any("remote" in loc.lower() for loc in job["location"]),
                technologies = job["technologies"] if "technologies" in job else [],
                employment_type = 'FULL_TIME',
                description = job["description"]
            )
            result.append(listing)
        return result
    
    def filter_eu_jobs(self, jobs):
        filtered_jobs = []
        for job in jobs:
            for loc in job['location']:
                if any(country in loc for country in self.eu_countries):
                    filtered_jobs.append(job)
                    break
        return filtered_jobs

    def get_vacancies(self):
        jobs = self.filter_tech_jobs(self.scrape())
        jobs = self.filter_eu_jobs(jobs, 'location')
        jobs = self.transform_data(jobs)
        self.update_db(jobs)
        print('Jetbrains jobs saved')
        return jobs

