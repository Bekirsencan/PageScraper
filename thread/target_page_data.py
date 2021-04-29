from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re


def get_page_data(scraper):
    webdriver_wait = WebDriverWait(scraper, 10)
    json_data = {
        "title": get_title(webdriver_wait),
        "brand": get_brand(webdriver_wait),
        "stars": get_stars(scraper),
        "stock": get_stock(webdriver_wait),
        "stock_amount": get_stock_amount(scraper),
        "seller": get_seller(webdriver_wait),
        "sender": get_sender(webdriver_wait),
        "price": get_price(webdriver_wait),
        "ratings": get_ratings(webdriver_wait)
        # "target_country": check_target_country(webdriver_wait)
    }
    return json_data


def get_price(webdriver_wait):
    element = webdriver_wait.until(EC.presence_of_element_located((By.ID, "price")))
    data = re.split(r'\D+', element)
    if data.__len__() == 6:
        total_price = float(data[1]) + float(data[2]) / 100 + float(data[3]) + float(data[4]) / 100
        return round(total_price, 2)
    else:
        total_price = float(data[3]) + float(data[4]) / 100 + float(data[5]) + float(data[6]) / 100
        return round(total_price, 2)


def get_title(webdriver_wait):
    return webdriver_wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text


def get_brand(webdriver_wait):
    var = webdriver_wait.until(EC.presence_of_element_located((By.ID, "bylineInfo"))).text.split()
    if len(var) == 4:
        return var[2]
    else:
        return var[1]


def get_stars(scraper):
    try:
        stars = scraper.find_element_by_id("acrPopover")
    except NoSuchElementException:
        return False
    return stars.get_attribute('title')


# def check_target_country(webdriver_wait):
#     if webdriver_wait.until(
#             EC.presence_of_element_located((By.ID, "exports_desktop_qualifiedBuybox_tlc_feature_div"))):
#         return True
#     else:
#         return False


def get_ratings(webdriver_wait):
    return webdriver_wait.until(EC.presence_of_element_located((By.ID, "acrCustomerReviewText"))).text


def get_stock(webdriver_wait):
    return webdriver_wait.until(EC.presence_of_element_located((By.ID, "availability"))).text


def get_stock_amount(scraper):
    try:
        select_box = scraper.find_element_by_id("quantity")
    except NoSuchElementException:
        return "1"
    options = [x for x in select_box.find_elements_by_tag_name("option")]
    return len(options)


def get_seller(webdriver_wait):
    return webdriver_wait.until(EC.presence_of_element_located((By.ID, "sellerProfileTriggerId"))).text


def get_sender(webdriver_wait):
    return webdriver_wait.until(EC.presence_of_element_located((By.ID, "SSOFpopoverLink"))).text
