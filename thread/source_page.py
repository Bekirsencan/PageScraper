from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import webdriver as webdriver_class
import queue_class as new_class
import re


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


class sourcePage:
    def __init__(self, scraper, data):
        self.data = data
        self.scraper = scraper
        self.webdriver_wait = WebDriverWait(scraper, 10)
        self.data_queue = new_class.data_queue.getInstance()

    def get_page(self):
        self.scraper.get(f"https://www.amazon.com/dp/{self.data}?psc=1")
        return self.check_page_status()

    def check_page_status(self):
        if self.scraper.title == "Page Not Found":
            pass
        elif self.scraper.title == "Sorry! Something went wrong!":
            self.scraper.refresh()
            webdriver_class.check_target(self.scraper)
            return self.check_target_country()
        else:
            webdriver_class.check_target(self.scraper)
            return self.check_target_country()

    def get_page_data(self):
        self.check_twister()
        json_data = {
            'title': self.get_title(),
            'brand': self.get_brand(),
            'stars': self.get_stars(),
            'stock': self.get_stock(),
            'stock_amount': self.get_stock_amount(),
            'seller': self.get_seller(),
            'sender': self.get_sender(),
            'price': self.get_price_data(),
            'ratings': self.get_ratings(),
            'target_country': self.check_target_country()
        }
        return json_data

    def check_target_country(self):
        try:
            self.scraper.find_element_by_id("exports_desktop_qualifiedBuybox_deliveryBlockContainer")
        except NoSuchElementException:
            return False
        return True

    def get_price_data(self):
        try:
            data = self.scraper.find_element_by_id("priceblock_ourprice").text
        except NoSuchElementException:
            data = self.scraper.find_element_by_id("priceblock_saleprice").text
            return self.get_saleprice(data)
        return self.get_ourprice(data)

    def get_saleprice(self, data):
        price = data[1::]
        try:
            fee = self.scraper.find_element_by_id("saleprice_shippingmessage").text
        except NoSuchElementException:
            fee = "$0 S"
        total_price = float(price) + float(re.search('\$(.*) s', fee.lower()).group(1))
        return round(total_price, 2)

    def get_ourprice(self, data):
        price = data[1::]
        try:
            fee = self.scraper.find_element_by_id("ourprice_shippingmessage").text
        except NoSuchElementException:
            fee = "$0 S"
        total_price = float(price) + float(re.search('\$(.*) s', fee.lower()).group(1))
        return round(total_price, 2)

    def get_title(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text

    def get_brand(self):
        var = self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "bylineInfo"))).text.split()
        if len(var) == 4:
            return var[2]
        else:
            return var[1]

    def get_stars(self):
        try:
            stars = self.scraper.find_element_by_id("acrPopover")
        except NoSuchElementException:
            return "0"
        return stars.get_attribute('title')

    def get_ratings(self):
        try:
            element = self.scraper.find_element_by_id("acrCustomerReviewText")
        except NoSuchElementException:
            return "0"
        return element.text

    def get_stock(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "availability"))).text

    def get_stock_amount(self):
        try:
            select_box = self.scraper.find_element_by_id("quantity")
        except NoSuchElementException:
            return "1"
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        return len(options)

    def get_seller(self):
        try:
            data = self.scraper.find_element_by_id("exports_desktop_qualifiedBuybox_tabular_feature_div")
        except NoSuchElementException:
            data = self.scraper.find_element_by_id("shipsFromSoldByInsideBuyBox_feature_div")
            return get_seller_profile_trigger(data)
        return get_seller_truncate(data)

    def get_sender(self):
        try:
            data = self.scraper.find_element_by_id("exports_desktop_qualifiedBuybox_tabular_feature_div")
        except NoSuchElementException:
            data = self.scraper.find_element_by_id("shipsFromSoldByInsideBuyBox_feature_div")
            return get_sender_popover(data)
        return get_sender_truncate(data)

    def check_twister(self):
        try:
            self.scraper.find_element_by_id("twister_feature_div")
        except NoSuchElementException:
            pass
        self.get_twister_asin()

    def get_twister_asin(self):
        twister_element_list = self.scraper.find_elements_by_css_selector(".swatchAvailable")
        for data in twister_element_list:
            self.data_queue.add_data_to_list(data.get_attribute("data-defaultasin"))

    # def check_queue(self,data):
    #     if not data in self.data_queue:
    #         self.data_queue.add_data(data)
    #     else:
    #         print("var")
