from bs4 import BeautifulSoup
import requests
from requests.models import Response
import json
from .scraper import Scraper
from jobs.models import Job


class JetbrainsScraper(Scraper):

    URL = "https://www.jetbrains.com/careers/jobs/"
    
    def scrape(self):
        page_source: Response =  requests.get(self.URL)
        soup: BeautifulSoup = BeautifulSoup(page_source.text, "lxml")

        def find_vacancies_script(tag):
            return (tag.name == "script" and 
                    "var VACANCIES =" in tag.string if tag.string else False)

        vacancies_script = soup.find(find_vacancies_script)
        json_vacancies = json.loads(vacancies_script.contents[0].split("var VACANCIES = ")[1].strip())
        return json_vacancies
    
    def transform_data(self, jobs) -> list:
        for job in jobs:
            if len(job["role"]) > 2: print(f"{job['role']}")
            job["role"] = job["role"][0]
            job["remote"] = "remote" in job["location"].lower()
            job["company"] = "Jetbrains"
            del job["team"]
            del job["language"]
            if "technologies" not in job: job["technologies"] = []
        return jobs
    
    def get_vacancies(self):
        jobs = self.filter_tech_jobs(self.scrape())
        return self.transform_data(jobs)

