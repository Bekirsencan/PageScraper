from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import json
from selenium import webdriver
import consumer.aod as aod_class


def main(scraper: webdriver):
    wait = WebDriverWait(scraper, 30)
    wait.until(ec.element_to_be_clickable((By.ID,"aod-pinned-offer-show-more-link"))).click()
    data = scraper.find_element_by_id("aod-pinned-offer")
    json_data = {
        "seller": get_pinned_seller(data),
        "sender": get_pinned_sender(data),
        "ratings": get_pinned_ratings(data),
        "price": get_pinned_price(data)
    }
    print(json.dumps(json_data))
    aod_list = scraper.find_elements_by_id("aod-offer")
    return aod_class.main(aod_list)


def check_existing(scraper: webdriver):
    try:
        scraper.find_element_by_id("olpLinkWidget_feature_div").click()
    except NoSuchElementException:
        return  ### (new url function)
    return main(scraper)


def get_pinned_seller(aod_element):
    var = aod_element.find_element_by_id("aod-offer-soldBy")
    return var.find_element_by_css_selector("a.a-size-small.a-link-normal").text

def get_pinned_ratings(aod_element):
    var = aod_element.find_element_by_id("seller-rating-count-{iter}").text
    var_element = var.split()
    return var_element[0][1::]


def get_pinned_sender(aod_element):
    data = aod_element.find_element_by_css_selector("#aod-offer-shipsFrom")
    return data.find_element_by_css_selector("span.a-size-small.a-color-base").text


def get_pinned_price(aod_element):
    price_text = aod_element.find_element_by_css_selector("[data-a-size]").text.split()
    price_float = float(price_text[0][1::] + "." + price_text[1])
    fee_text = aod_element.find_element_by_css_selector("span.a-color-secondary.a-size-base").text.split()
    fee_float = float(fee_text[1][1::])
    total_price = fee_float + price_float
    return round(total_price, 2)
