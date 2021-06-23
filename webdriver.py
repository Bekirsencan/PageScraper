from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time


def change_target_location(page_scraper: webdriver):  # for usa
    time.sleep(5)
    wait_element = WebDriverWait(page_scraper, 60)
    wait_element.until(ec.element_to_be_clickable((By.ID, "nav-global-location-data-modal-action"))).click()
    time.sleep(2)
    wait_element.until(ec.element_to_be_clickable((By.ID, "GLUXCountryListDropdown"))).click()
    page_scraper.find_element_by_css_selector("ul.a-nostyle.a-list-link").find_element_by_xpath(
        f"li[contains(.,'{'Canada'}')]").click()
    wait_element.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[name='glowDoneButton']"))).click()
    page_scraper.refresh()


def check_target(page_scraper: webdriver):
    target_country = page_scraper.find_element_by_id("glow-ingress-line2")
    if target_country.text == "Canada":
        return True
    else:
        return change_target_location(page_scraper)


def change_postal_code(page_scraper: webdriver, zip_code):  # for canada
    time.sleep(5)
    try:
        a = page_scraper.find_element_by_id("nav-global-location-data-modal-action").click()
    except:
        print("hata")
    return postal_code_input(page_scraper, zip_code)


def postal_code_input(page_scraper, zip_code):
    try:
        page_scraper.find_element_by_id("GLUXZipUpdateInput")
    except NoSuchElementException:
        return two_postal_code(page_scraper, zip_code)
    return one_postal_code(page_scraper, zip_code)


def check_postal_code(page_scraper: webdriver, zip_code):
    target_zip_code = page_scraper.find_element_by_id("glow-ingress-line2")
    if target_zip_code == zip_code:
        pass
    else:
        change_postal_code(page_scraper, zip_code)


def one_postal_code(page_scraper, zip_code):
    time.sleep(5)
    page_scraper.find_element_by_id("GLUXZipUpdateInput").send_keys(zip_code)
    page_scraper.find_element_by_id("GLUXZipUpdate").click()
    time.sleep(10)

def two_postal_code(page_scraper, zip_code):
    time.sleep(5)
    data = zip_code.split()
    page_scraper.find_element_by_id("GLUXZipUpdateInput_0").send_keys(data[0])
    page_scraper.find_element_by_id("GLUXZipUpdateInput_1").send_keys(data[1])
    page_scraper.find_element_by_id("GLUXZipUpdate").click()
    time.sleep(10)
