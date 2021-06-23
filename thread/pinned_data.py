from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import re


def main(scraper):
    wait = WebDriverWait(scraper, 10)
    wait.until(ec.element_to_be_clickable((By.ID, "aod-pinned-offer-show-more-link"))).click()
    pinned_data = wait.until(ec.presence_of_element_located((By.ID, "aod-pinned-offer")))
    pinned_json = [{
        "price": get_pinned_price(pinned_data),
        "seller": get_pinned_seller(pinned_data),
        "sender": get_pinned_sender(pinned_data)
    }]
    aod_list = scraper.find_elements_by_id("aod-offer")
    for data in aod_list:
        aod_json = {
            "price": get_aod_price(data),
            "seller": get_aod_seller(data),
            "sender": get_aod_sender(data)
        }
        pinned_json.append(aod_json)
    return pinned_json


def get_pinned_seller(pinned_data):
    var = pinned_data.find_element_by_id("aod-offer-soldBy")
    try:
        aod_seller = var.find_element_by_css_selector(".a-size-small.a-link-normal").text
    except NoSuchElementException:
        return "Amazon"
    return aod_seller


def get_pinned_sender(pinned_data):
    data = pinned_data.find_element_by_id("aod-offer-shipsFrom")
    return data.find_element_by_css_selector("span.a-size-small.a-color-base").text


def get_pinned_price(pinned_data):
    price_data = pinned_data.find_element_by_css_selector(".a-price").text
    price = price_data.replace('\n', ".")
    price2 = float(price[1::])
    fee_text = pinned_data.find_element_by_id("aod-rafn-shipping-plus-ifd-might-apply-0").text
    fee = check_fee(fee_text)
    total_price = float(price2) + float(fee)
    return total_price


def check_fee(fee_text):
    try:
        fee = re.search('\$(.*) s', fee_text.lower()).group(1)
    except NoSuchElementException:
        return "0"
    return fee


def get_aod_price(aod_data):
    price_text = aod_data.find_element_by_css_selector("span.a-price").text
    price = price_text.replace('\n', ".")
    fee_text = aod_data.find_element_by_id("delivery-message").text
    fee = check_aod_fee(fee_text)
    return float(fee)+float(price[1::])


def check_aod_fee(fee_text):
    try:
        fee = re.search('\$(.*) d', fee_text.lower()).group(1)
    except NoSuchElementException:
        return "0"
    return fee


def get_aod_sender(aod_data):
    data = aod_data.find_element_by_id("aod-offer-shipsFrom")
    return data.find_element_by_css_selector("span.a-size-small.a-color-base").text


def get_aod_seller(aod_data):
    var = aod_data.find_element_by_id("aod-offer-soldBy")
    try:
        aod_seller = var.find_element_by_css_selector(".a-size-small.a-link-normal").text
    except NoSuchElementException:
        return "Amazon"
    return aod_seller
