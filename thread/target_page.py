from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import webdriver as webdriver_class
import pinned_data as pinned

from json_file import json_file


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


class targetPage:
    def __init__(self, scraper, data):
        self.data = data
        self.page_data = None
        self.scraper = scraper
        self.webdriver_wait = WebDriverWait(scraper, 10)
        self.json_file = json_file.getInstance()

    def get_page(self):
        self.scraper.get(f"https://www.amazon.ca/dp/{self.data}")
        self.check_page_status()

    def check_page_status(self):
        if self.scraper.title == "Page Not Found":
            self.json_file.delete_one_data(self.data)
        elif self.scraper.title == "Sorry! Something went wrong!":
            self.scraper.refresh()
            webdriver_class.change_postal_code(self.scraper, "K0G 0A0")
            self.show_data()
        else:
            webdriver_class.check_postal_code(self.scraper, "K0G 0A0")
            self.show_data()

    def show_data(self):
        self.get_page_data()
        return self.page_data

    def get_page_data(self):
        json_data = {
            "title": self.get_title(),
            "brand": self.get_brand(),
            "stars": self.get_stars(),
            "ratings": self.get_ratings(),
            "datas": []
        }
        price_data = self.check_quantity()
        json_data["datas"].append(price_data)
        pinned_json = self.check_pinned_data()
        json_data["datas"].append(pinned_json)
        print(json_data)
        return json_data

    def check_quantity(self):
        data = self.get_stock_amount()
        if not data == "0":
            json_data = {
                "price": self.get_price_data(),
                "sender": self.get_sender(),
                "seller": self.get_seller()
            }
            return json_data

    def check_pinned_data(self):
        try:
            self.scraper.find_element_by_css_selector(".a-touch-link.a-box.olp-touch-link").click()
        except NoSuchElementException:
            return self.json_file.delete_one_data(self.data)
        return self.get_pinned_data()

    def get_pinned_data(self):
        return pinned.main(self.scraper)

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
            fee = "0"
        return self.total_price(price, fee)

    def get_ourprice(self, data):
        price = data[1::]
        try:
            fee = self.scraper.find_element_by_id("ourprice_shippingmessage").text
        except NoSuchElementException:
            fee = "0"
        return self.total_price(price, fee)

    def total_price(self, price, fee):
        if not fee == "0":
            return float(price)
        else:
            return float(price) + float(fee.split()[1][1::])

    def get_title(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text

    def get_brand(self):
        try:
            var = self.scraper.find_element_by_id("bylineInfo")
        except NoSuchElementException:
            return "None"
        brand = var.text.split()
        if len(brand) == 4:
            return brand[2]
        elif len(brand) == 3:
            return brand[1] + " " + brand[2]
        elif len(brand) == 2:
            return brand[1]

    def get_stars(self):
        try:
            stars = self.scraper.find_element_by_id("acrPopover")
        except NoSuchElementException:
            return "0"
        return stars.get_attribute('title')

    def get_ratings(self):
        try:
            ratings = self.scraper.find_element_by_id("acrCustomerReviewText").text
        except NoSuchElementException:
            return "0"
        return ratings

    def get_stock(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "availability"))).text

    def get_stock_amount(self):
        try:
            select_box = self.scraper.find_element_by_id("quantity")
        except NoSuchElementException:
            return "0"
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
