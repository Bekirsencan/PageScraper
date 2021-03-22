from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import json
from selenium import webdriver
import aod as aod_class

ratings = None
seller = None


def main(scraper: webdriver):
    wait = WebDriverWait(scraper, 30)
    wait.until(ec.element_to_be_clickable((By.ID,""))).click()
    get_pinned_seller(scraper)
    get_pinned_price(scraper)
    json_data = {
        "seller": seller,
        "sender": get_pinned_sender(scraper),
        "ratings": ratings,
        "price": get_pinned_price(scraper)
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


def get_pinned_seller(scraper: webdriver):
    global ratings
    global seller
    var = scraper.find_element_by_xpath(
        "/html/body/div[1]/span/span/span/div/div/div[2]/div/div[3]/div[1]/div[5]/div/div/div/div[2]").text.split()
    ratings = var[1][1::]
    seller = var[0]


def get_pinned_sender(scraper: webdriver):
    return scraper.find_element_by_xpath(
        "/html/body/div[1]/span/span/span/div/div/div[2]/div/div[3]/div[1]/div[4]/div/div/div/div[2]/span").text


def get_pinned_price(scraper: webdriver):
    var = scraper.find_element_by_xpath("//div[@id='pinned-offer-top-id']/div[1]").text
    price_text = var.split()
    price_float = float(price_text[0][1::] + "." + price_text[1])
    fee = scraper.find_element_by_xpath(
        "/html/body/div[1]/span/span/span/div/div/div[2]/div/div[1]/div/div[2]/div[3]/div/div[1]/div/div[3]/span/span").text
    fee_text = fee.split()
    fee_float = float(fee_text[1][1::])
    all_price = fee_float + price_float
    return round(all_price, 2)
