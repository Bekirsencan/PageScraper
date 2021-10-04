from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import re


def get_data(scraper):
    wait = WebDriverWait(scraper, 10)
    wait.until(ec.element_to_be_clickable((By.ID, "aod-pinned-offer-show-more-link"))).click()
    pinned_data = wait.until(ec.presence_of_element_located((By.ID, "aod-pinned-offer")))
    json_array = []
    pinned_json = get_pinned_data(pinned_data)
    json_array.append(pinned_json)
    aod_list = scraper.find_elements_by_id("aod-offer")
    aod_array = get_aod_data(aod_list)
    json_array = json_array + aod_array
    return json_array


def get_pinned_data(pinned_data):
    js = {
        'price': get_pinned_price(pinned_data),
        'sender': get_pinned_sender(pinned_data),
        'seller': get_pinned_seller(pinned_data)
    }
    return js


def get_aod_data(aod_list):
    array = []
    for data in aod_list:
        aod_json = {
            'price': get_aod_price(data),
            'seller': get_aod_seller(data),
            'sender': get_aod_sender(data)
        }
        array.append(aod_json)
    return array


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
    price = price.replace(',', "")
    price2 = re.split("[$,£]", price)[1]
    fee = check_fee(pinned_data)
    total_price = float(price2) + float(fee)
    return total_price


def check_fee(pinned_data):
    try:
        fee_text = pinned_data.find_element_by_id("aod-rafn-shipping-plus-ifd-might-apply-0").text
        fee = re.search('[$,£](.*) s', fee_text.lower()).group(1)
    except:
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


def get_aod_price(aod_data):
    price_text = aod_data.find_element_by_css_selector("span.a-price").text
    price = price_text.replace('\n', ".")
    price = price.replace(',', "")
    price = re.split("[$,£]", price)[1]
    fee = check_aod_fee(aod_data)
    total_price = float(fee) + float(price)
    return total_price


def check_aod_fee(aod_data):
    try:
        fee_text = aod_data.find_element_by_id("delivery-message").text
        fee = re.search('[$,£](.*) d', fee_text.lower()).group(1)
    except:
        return "0"
    return fee
