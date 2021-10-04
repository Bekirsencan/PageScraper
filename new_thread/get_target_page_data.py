import logging
import re
import time

import target_pinned_data
from json_filee import json_file

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

js = json_file.getInstance()
bool_cookies = False


def check_data(scraper):
    check_cookies(scraper)
    boolean = check_quantity(scraper)
    if boolean:
        return get_all_data(scraper)
    #### REM1 -> return olarak boş json ve false döndürülebilr. None datayı hem target hemde source jsondan silebilriiz.


def check_cookies(scraper):
    global bool_cookies
    if not bool_cookies:
        boolean = cookies(scraper)
        if boolean:
            scraper.find_element_by_css_selector(".a-button-input.celwidget").click()


def cookies(scraper):
    global bool_cookies
    try:
        scraper.find_element_by_css_selector(".a-button-input.celwidget")
    except:
        return False
    return True


def get_all_data(scraper):
    wait = WebDriverWait(scraper, 10)
    json_data = {
        'title': get_title(wait),
        'brand': get_brand(scraper),
        'stars': get_stars(scraper),
        'ratings': get_ratings(scraper),
        'datas': []
    }
    json = {'price': get_price_data(scraper), 'sender': get_sender(scraper), 'seller': get_seller(scraper)}
    json_data["datas"].append(json)
    if target_pinned_data.check_pinned_data(scraper):
        json_array = target_pinned_data.get_pinned_data(scraper)
        json_data["datas"] = json_data["datas"] + json_array
    return json_data


def check_quantity(scraper):
    stock_amount = get_stock_amount(scraper)
    if not int(stock_amount) == 0:
        return True
    else:
        return False


def get_price_data(scraper):
    try:
        data = scraper.find_element_by_id("priceblock_ourprice").text
    except NoSuchElementException:
        data = scraper.find_element_by_id("priceblock_saleprice").text
        return get_saleprice(scraper, data)
    return get_ourprice(scraper, data)


def get_ourprice(scraper, data):
    price = re.split("[D$£]", data)[1]
    price = price.replace(",", "")
    fee = scraper.find_element_by_id("ourprice_shippingmessage").text
    if fee:
        fee = re.split("[D$£]", fee)[1]  # re.split("[$,£]", fee)[1]
        fee = fee.split()[0]
    else:
        fee = check_fee(scraper)
    fee = re.split("[D$£]", fee)[1]
    fee = fee.split()[0]
    return total_price(price, fee)


def get_saleprice(scraper, data):
    price = re.split("[D$£]", data)[1]
    price = price.replace(",", "")
    fee = scraper.find_element_by_id("saleprice_shippingmessage").text
    if fee:
        fee = re.split("[D$£]", fee)[1]
        fee = fee.split()[0]
    else:
        fee = check_fee(scraper)
    fee = re.split("[D$£]", fee)[1]
    fee = fee.split()[0]
    return total_price(price, fee)


def total_price(price, fee):
    return round(float(price) + float(fee), 2)


def check_fee(scraper):
    try:
        fee = scraper.find_element_by_id("priceblock_ourprice_ifdmsg").text
    except NoSuchElementException:
        fee = "$0"
        return fee
    return fee


def get_sender(scraper):
    try:
        data = scraper.find_element_by_id("tabular-buybox")
    except NoSuchElementException:
        data = scraper.find_element_by_id("shipsFromSoldByInsideBuyBox_feature_div")
        return get_sender_popover(data)
    return get_sender_truncate(data)


def get_seller(scraper):
    try:
        data = scraper.find_element_by_id("tabular-buybox")
    except NoSuchElementException:
        data = scraper.find_element_by_id("shipsFromSoldByInsideBuyBox_feature_div")
        return get_seller_profile_trigger(data)
    return get_seller_truncate(data)


def get_seller_truncate(data):
    return data.find_element_by_id("tabular-buybox-truncate-1").text


def get_seller_profile_trigger(data):
    try:
        seller = data.find_element_by_id("sellerProfileTriggerId").text
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


def get_stock_amount(scraper):
    try:
        select_box = scraper.find_element_by_id("quantity")
    except NoSuchElementException:
        return "0"
    options = [x for x in select_box.find_elements_by_tag_name("option")]
    return len(options)


def get_title(wait):
    return wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text


def get_brand(scraper):
    try:
        var = scraper.find_element_by_id("bylineInfo")
    except NoSuchElementException:
        return "None"
    brand = var.text.split()
    if len(brand) == 4:
        return brand[2]
    elif len(brand) == 3:
        return brand[1] + " " + brand[2]
    elif len(brand) == 2:
        return brand[1]


def get_stars(scraper):
    try:
        stars = scraper.find_element_by_id("acrPopover")
    except NoSuchElementException:
        return "0"
    return stars.get_attribute('title')


def get_ratings(scraper):
    try:
        ratings = scraper.find_element_by_id("acrCustomerReviewText").text
    except NoSuchElementException:
        return "0"
    return ratings
