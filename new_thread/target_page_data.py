from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import webdriver as webdriver_class
import get_target_page_data

from json_filee import json_file

js = json_file.getInstance()


def get_page(data_asin, scraper):
    scraper.get(f"https://www.amazon.com.au/dp/{data_asin}")
    return check_page_status(data_asin, scraper)


def check_page_status(data_asin, scraper):
    if scraper.title == "Page Not Found":
        js.delete_one_data(data_asin)
    elif scraper.title == "Sorry! Something went wrong!":
        scraper.refresh()
        webdriver_class.check_postal_code(scraper, "2055")
        return get_target_page_data.check_data(scraper)  # REM1
    else:
        webdriver_class.check_postal_code(scraper, "2055")
        return get_target_page_data.check_data(scraper)  # REM1
