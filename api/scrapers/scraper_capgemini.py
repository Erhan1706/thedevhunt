from .scraper import Scraper
from jobs.models import Job
from .scraper_registry import register_scraper
import pycountry 
import html

@register_scraper("capgemini")
class CapgeminiScraper(Scraper):
  company = "Capgemini"

  url = "https://www.capgemini.com/wp-json/macs/v1/jobs?country=BE%2CCZ%2CDK%2CAT%2Cen-fi%2Cfr-fr%2CDE%2CHU%2Cit-it%2CNL%2CNO%2Cpl-pl%2Cen-pt%2Cen-ro%2Ces-es%2CSE%2Cen-gb%2Cen-ch&size=3000"

  payload = {}
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.capgemini.com/careers/join-capgemini/job-search/?country_code=BE%2CCZ%2CDK%2CAT%2Cen-fi%2Cfr-fr%2CDE%2CHU%2Cit-it%2CNL%2CNO%2Cpl-pl%2Cen-pt%2Cen-ro%2Ces-es%2CSE%2Cen-gb%2Cen-ch&size=30',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
    'Cookie': 'TAsessionID=8f3d7a2d-7de6-4c96-bf82-5471b368e626|NEW; notice_behavior=implied,eu; gpcishonored=true; notice_preferences=0:; notice_gdpr_prefs=0:; cmapi_gtm_bl=ga-ms-ua-ta-asp-bzi-sp-awct-cts-csm-img-flc-fls-mpm-mpr-m6d-tc-tdc; cmapi_cookie_privacy=permit 1 required'
  }

  def parse_locations(self, location_string, country_code):
    """ Parse the location string from Capgemini API response. 
    The location string comes in the format "City, City, City". The country is only included as a country code (e.g. "en-gb")
    """
    locations = location_string.split(", ")
    codes = country_code.upper().split("-")
    if len(codes) == 2:
      # In every case, the second part is the country code, except for sweden for some reason.
      if country_code == "se-en":
        country_code = "SE"
      else:
        country_code = codes[1]

    parsed_locations = []
    # Get the country name from the country code
    country = pycountry.countries.get(alpha_2=country_code)
    for loc in locations:
      loc = loc.strip()
      if country: parsed_locations.append(f"{loc}, {country.name}")
    
    if not parsed_locations:
      print("No locations found for job")
      
    return parsed_locations

  def transform_data(self, jobs):
    result = []
    for job in jobs:
      # More inconsistencies with response data
      creation_date = None
      if type(job["updated_at"]) != str:
        creation_date = job["indexed_at"] if type(job["indexed_at"]) == str else None

      listing = Job(
        title= job['title'],
        slug= job['ref'],
        role= self.classify_role_smart(job["title"]),
        company= self.company,
        location= self.parse_locations(job["location"], job["country_code"]), 
        link_to_apply= job["apply_job_url"],
        employment_type= 'FULL_TIME', 
        remote = False, 
        description = html.unescape(job["description"]),
        created_at = creation_date
      )
      result.append(listing)

    return result

  def filter_tech_jobs(self, jobs):
    revelevant_capgemini_departments = {"Architect", "Architecture,Cloud","Cloud","Cloud Infrastructure Management", "SaaS Solutions", 
                                          "Cybersecurity", "Data & AI", "Data & analytics", "Embedded & Systems", "Hardware Engineering",
                                          "Infrastructure services,Cloud", "Quality Engineering & Testing", "Software Engineering", "Software development & testing", "Software development & testing,Cloud",
                                          "Test Engineering", "Digital experience & design,Software development & testing"}
    return [job for job in jobs if job['department'] in revelevant_capgemini_departments 
            or job["professional_communities"] in revelevant_capgemini_departments]

  def get_vacancies(self):
    data = self.scrape()
    tech_jobs = self.filter_tech_jobs(data["data"])
    jobs = self.transform_data(tech_jobs)
    self.update_db(jobs)
    print(f'{self.company} jobs saved')