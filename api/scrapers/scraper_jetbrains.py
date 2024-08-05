from bs4 import BeautifulSoup
import requests
from requests.models import Response
import json
from .scraper import Scraper

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
    
    def get_vacancies(self):
        jobs = self.scrape()
        return self.filter_tech_jobs(jobs)
