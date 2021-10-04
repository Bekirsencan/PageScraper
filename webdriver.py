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
        f"li[contains(.,'{'Australia'}')]").click()
    wait_element.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[name='glowDoneButton']"))).click()
    page_scraper.refresh()


def check_target(page_scraper: webdriver): # canada yerine hedef ülke olarak ekle
    target_country = page_scraper.find_element_by_id("glow-ingress-line2")
    if target_country.text == "Australia":
        return True
    else:
        return change_target_location(page_scraper)


def change_postal_code(page_scraper: webdriver, zip_code):  # for canada
    time.sleep(5)
    try:
        page_scraper.find_element_by_id("nav-global-location-data-modal-action").click()
    except:
        print("hata")
    return check_au(page_scraper, zip_code)


def check_au(scraper, zip_code):
    time.sleep(2)
    print("check_au")
    try:
        scraper.find_element_by_id("GLUXPostalCodeWithCity_PostalCodeInput")
    except:
        return check_ae(scraper, zip_code)
    return change_au(scraper, zip_code)


def check_ae(scraper, zip_code):
    time.sleep(2)
    print("check_ae")
    try:
        scraper.find_element_by_id("GLUXCityListDropdown")
    except:
        return postal_code_input(scraper, zip_code)
    return change_ae(scraper, zip_code)


def change_ae(scraper, zip_code):
    print("change_ae")
    scraper.find_element_by_id("GLUXCityListDropdown").click()
    time.sleep(5)
    scraper.find_element_by_id("GLUXCityList_0").click()


def change_au(scraper, zip_code):
    print("change_au")
    scraper.find_element_by_id("GLUXPostalCodeWithCity_PostalCodeInput").send_keys(zip_code)
    time.sleep(5)
    scraper.find_element_by_id("GLUXPostalCodeWithCity_DropdownButton").click()
    time.sleep(5)
    scraper.find_element_by_id("GLUXPostalCodeWithCity_DropdownList_0").click()
    time.sleep(5)
    scraper.find_element_by_id("GLUXPostalCodeWithCityApplyButton").click()
    time.sleep(10)


def postal_code_input(page_scraper, zip_code):
    time.sleep(2)
    try:
        page_scraper.find_element_by_css_selector(".GLUX_Full_Width.a-declarative")
    except NoSuchElementException:
        return two_postal_code(page_scraper, zip_code)
    return one_postal_code(page_scraper, zip_code)


def check_postal_code(page_scraper: webdriver, zip_code):
    target_zip_code = page_scraper.find_element_by_id("glow-ingress-line2").text
    if zip_code[0:-2] in target_zip_code:
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
