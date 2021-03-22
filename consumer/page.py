from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import json
import twister as twister_class
import webdriver as webdriver_class
import pinned as pinned_class


def get_page(page_scraper: webdriver, url):
    page_scraper.get(url)
    if webdriver_class.check_target(page_scraper):
        return twister_class.check_twister(page_scraper)
    else:
        webdriver_class.change_target_location(page_scraper)
        return twister_class.check_twister(page_scraper)


def get_page_data(page_scraper: webdriver):
    json_data = {
        "title": get_title(page_scraper),
        "brand": get_brand(page_scraper),
        "stars": get_stars(page_scraper),
        "stock": get_stock(page_scraper),
        "stock_amount": get_stock_amount(page_scraper),
        "seller": get_seller(page_scraper),
        "sender": get_sender(page_scraper),
        "price": get_price(page_scraper),
        "ratings": get_ratings(page_scraper),
        "target_country": check_target_country(page_scraper)
    }
    print(json.dumps(json_data))
    return pinned_class.check_existing(page_scraper)


# Sayfa verileri

def get_price(page_scraper: webdriver):
    price = page_scraper.find_element_by_id("priceblock_ourprice").text[1::]
    fee = page_scraper.find_element_by_id("ourprice_shippingmessage").text.split()[1][1::]
    total_price = float(price) + float(fee)
    return round(total_price, 2)


def get_title(page_scraper: webdriver):
    return page_scraper.find_element_by_id("productTitle").text


def get_brand(page_scraper: webdriver):
    return page_scraper.find_element_by_css_selector("table.a-normal.a-spacing-micro").find_element_by_xpath(
        "tbody/tr[2]/td[2]")


def get_stars(page_scraper: webdriver):
    stars = page_scraper.find_element_by_id("acrPopover")
    return stars.get_attribute('title')


def check_target_country(page_scraper: webdriver):
    if page_scraper.find_element_by_id("exports_desktop_qualifiedBuybox_tlc_feature_div"):
        return True
    else:
        return False


def get_ratings(page_scraper: webdriver):
    return page_scraper.find_element_by_id("acrCustomerReviewText").text


def get_stock(page_scraper: webdriver):
    return page_scraper.find_element_by_id("availability").text


def get_stock_amount(page_scraper: webdriver):
    select_box = page_scraper.find_element_by_id("quantity")
    options = [x for x in select_box.find_elements_by_tag_name("option")]
    return len(options)


def get_seller(page_scraper: webdriver):
    return page_scraper.find_element_by_id("tabular-buybox-truncate-1").text


def get_sender(page_scraper: webdriver):
    return page_scraper.find_element_by_id("tabular-buybox-truncate-0").text
