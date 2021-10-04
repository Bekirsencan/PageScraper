import re

import twister_check
from json_filee import json_file

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

js = json_file.getInstance()


def get_data(data_asin, scraper):
    twister_check.check_twister(scraper)
    return get_all_data(data_asin, scraper)


def get_all_data(data_asin, scraper):
    wait = WebDriverWait(scraper, 10)
    json_data = {
        'title': get_title(wait),
        'brand': get_brand(wait),
        'stars': get_stars(scraper),
        'stock': get_stock(wait),
        'stock_amount': get_stock_amount(scraper),
        'seller': get_seller(scraper),
        'sender': get_sender(scraper),
        'price': get_price_data(scraper),
        'ratings': get_ratings(scraper),
        'target_country': "true"
    }
    return json_data


def get_price_data(scraper):
    try:
        data = scraper.find_element_by_id("priceblock_ourprice").text
    except NoSuchElementException:
        data = scraper.find_element_by_id("priceblock_saleprice").text
        return get_saleprice(scraper, data)
    return get_ourprice(scraper, data)


def get_saleprice(scraper, data):
    price = data.split("$",1)[1]
    price = price.replace(",", "")
    try:
        fee = scraper.find_element_by_id("saleprice_shippingmessage").text
    except NoSuchElementException:
        fee = "$0 S"
    total_price = float(price) + float(re.search('\$(.*) shi', fee.lower()).group(1))
    return round(total_price, 2)


def get_ourprice(scraper, data):
    price = data.split("$",1)[1]
    price = price.replace(",", "")
    try:
        fee = scraper.find_element_by_id("ourprice_shippingmessage").text
    except NoSuchElementException:
        fee = "$0 S"
    total_price = float(price) + float(re.search('\$(.*) shi', fee.lower()).group(1))
    return round(total_price, 2)


def get_title(wait):
    return wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text


def get_brand(wait):
    var = wait.until(EC.presence_of_element_located((By.ID, "bylineInfo"))).text.split()
    if len(var) == 4:
        return var[2]
    else:
        return var[1]


def get_stars(scraper):
    try:
        stars = scraper.find_element_by_id("acrPopover")
    except NoSuchElementException:
        return "0"
    return stars.get_attribute('title')


def get_ratings(scraper):
    try:
        element = scraper.find_element_by_id("acrCustomerReviewText")
    except NoSuchElementException:
        return "0"
    return element.text


def get_stock(wait):
    return wait.until(EC.presence_of_element_located((By.ID, "availability"))).text


def get_stock_amount(scraper):
    try:
        select_box = scraper.find_element_by_id("quantity")
    except NoSuchElementException:
        return "1"
    options = [x for x in select_box.find_elements_by_tag_name("option")]
    return len(options)


def get_seller(scraper):
    try:
        data = scraper.find_element_by_id("exports_desktop_qualifiedBuybox_tabular_feature_div")
    except NoSuchElementException:
        data = scraper.find_element_by_id("shipsFromSoldByInsideBuyBox_feature_div")
        return get_seller_profile_trigger(data)
    return get_seller_truncate(data)


def get_sender(scraper):
    try:
        data = scraper.find_element_by_id("exports_desktop_qualifiedBuybox_tabular_feature_div")
    except NoSuchElementException:
        data = scraper.find_element_by_id("shipsFromSoldByInsideBuyBox_feature_div")
        return get_sender_popover(data)
    return get_sender_truncate(data)


def get_seller_truncate(data):
    return data.find_element_by_id("tabular-buybox-truncate-1").text


def get_seller_profile_trigger(data):
    try:
        seller = data.find_element_by_id("sellerProfileTriggerId")
    except NoSuchElementException:
        return "Amazon"
    return seller


def get_sender_truncate(data):
    return data.find_element_by_id("tabular-buybox-truncate-0").text


def get_sender_popover(data):
    try:
        sender = data.find_element_by_id("SSOFpopoverLink").text
    except NoSuchElementException:
        return "Amazon"
    return sender
