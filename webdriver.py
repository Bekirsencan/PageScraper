from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def change_target_location(page_scraper: webdriver):
    wait_element = WebDriverWait(page_scraper, 10)
    wait_element.until(ec.element_to_be_clickable((By.ID, "nav-global-location-data-modal-action"))).click()
    wait_element.until(ec.element_to_be_clickable((By.ID, "GLUXCountryListDropdown"))).click()
    page_scraper.find_element_by_css_selector("ul.a-nostyle.a-list-link").find_element_by_xpath(
        f"li[contains(.,'{'Turkey'}')]").click()
    wait_element.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[name='glowDoneButton']"))).click()
    page_scraper.refresh()


def check_target(page_scraper: webdriver):
    target_country = page_scraper.find_element_by_id("glow-ingress-line2")
    if target_country.text == "Turkey":
        return True
    else:
        return False
