from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import webdriver as webdriver_class
import queue_classs as queue_class
import get_source_page_data
import re


def get_page(data_asin, scraper):
    scraper.get(f"https://www.amazon.com/dp/{data_asin}?psc=1")
    return check_page_status(data_asin, scraper)


def check_page_status(data_asin, scraper):
    if scraper.title == "Page Not Found":
        pass
    elif scraper.title == "Sorry! Something went wrong!":
        scraper.refresh()
        webdriver_class.check_target(scraper)
        return target_country(data_asin, scraper)
    else:
        webdriver_class.check_target(scraper)
        return target_country(data_asin, scraper)


def target_country(data_asin, scraper):
    boolean = check_target_country(scraper)
    if boolean:
        return get_source_page_data.get_data(data_asin, scraper)
    #### eğer yoksa target listeden çıkar


def check_target_country(scraper):
    try:
        scraper.find_element_by_id("exports_desktop_qualifiedBuybox_deliveryBlockContainer")
    except NoSuchElementException:
        return False
    return True
