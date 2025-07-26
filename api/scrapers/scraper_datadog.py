from .scraper import Scraper
from jobs.models import Job
from .scraper_registry import register_scraper
import html

@register_scraper("datadog")
class DatadogScraper(Scraper):
  company = "Datadog"
  
  url = "https://gk6e3zbyuntvc5dap.a1.typesense.net/multi_search?x-typesense-api-key=1Hwq7hntXp211hKvRS3CSI2QSU7w2gFm"

  payload = "{\"searches\":[{\"preset\":\"careers_list_view\",\"collection\":\"careers_alias\",\"q\":\"*\",\"facet_by\":\"child_department_Engineering,child_department_GeneralAdministrative,child_department_Marketing,child_department_Sales,child_department_TechnicalSolutions,location_APAC,location_Americas,location_EMEA,parent_department_Engineering,parent_department_GeneralAdministrative,parent_department_Marketing,parent_department_ProductDesign,parent_department_ProductManagement,parent_department_Sales,parent_department_TechnicalSolutions,region_APAC,region_Americas,region_EMEA,remote,time_type\",\"filter_by\":\"language: en && parent_department_Engineering:=[`Engineering`] && region_EMEA:=[`EMEA`]\",\"max_facet_values\":50,\"page\":1,\"per_page\":250},{\"preset\":\"careers_list_view\",\"collection\":\"careers_alias\",\"q\":\"*\",\"facet_by\":\"parent_department_Engineering\",\"filter_by\":\"language: en && region_EMEA:=[`EMEA`]\",\"max_facet_values\":50,\"page\":1},{\"preset\":\"careers_list_view\",\"collection\":\"careers_alias\",\"q\":\"*\",\"facet_by\":\"region_EMEA\",\"filter_by\":\"language: en && parent_department_Engineering:=[`Engineering`]\",\"max_facet_values\":50,\"page\":1}]}"
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'text/plain',
    'origin': 'https://careers.datadoghq.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://careers.datadoghq.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36'
  }
  
  def determine_remote(self, location) -> bool:
    # They store the location in the format "City, Country/Remote; City, Country/Remote"
    # Determine if second location is remote for all listed locations
    locations = location.split(";")
    remote = False
    for loc in locations:
      if "remote" in loc.lower():
        remote = True
    return remote

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      job = job["document"]
      listing = Job(
        title= job['title'],
        slug= job['job_id'],
        role= job["department"],
        company= self.company,
        location= job["location_string"].split(";"),
        link_to_apply= job["absolute_url"],
        employment_type= 'FULL_TIME', 
        remote = self.determine_remote(job["location_string"]),
        description = (f"<br>{html.unescape(job['description']).replace('&nbsp;', '<br>')}"),
        created_at = job["last_mod"]
      )
      result.append(listing)

    return result
  
  def get_vacancies(self):
    data = self.scrape("POST")
    jobs = self.transform_data(data["results"][0]["hits"])
    self.update_db(jobs)
    print(f'{self.company} jobs saved')
