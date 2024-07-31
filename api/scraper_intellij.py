from bs4 import BeautifulSoup
import requests
from requests.models import Response
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json

URL = "https://www.jetbrains.com/careers/jobs/"

"""
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-notifications")
driver: WebDriver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(URL)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "jetbrains-cookies-banner-4-button"))).click()

show_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_sizeM_1o2xc3v_99")))
while True:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "_sizeM_1o2xc3v_99"))).click()
    button= driver.find_element(By.CLASS_NAME, "_sizeM_1o2xc3v_99") 
    if button.text != "Show more":
        break
        
driver.quit()
"""

def get_vacancies():
    page_source: Response =  requests.get(URL)
    soup: BeautifulSoup = BeautifulSoup(page_source.text, "lxml")

    def find_vacancies_script(tag):
        return (tag.name == "script" and 
                "var VACANCIES =" in tag.string if tag.string else False)

    vacancies_script = soup.find(find_vacancies_script)
    json_vacancies = json.loads(vacancies_script.contents[0].split("var VACANCIES = ")[1].strip())
    return json_vacancies

## TO DO: Filter based on location and tech positions 

