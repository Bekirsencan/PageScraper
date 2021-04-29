import proxy
import queue
import threading

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import queue_class as new_cls
import webdriver as webdriver_class
import consumer.twister as twister_class

a = queue.Queue()
t_json = {}


class Model(threading.Thread):
    def __init__(self, PORT):
        super().__init__()
        self.lock = threading.Lock()
        self.data = None
        self.scraper = proxy.new_proxy("127.0.0.1", PORT)
        self.data_qu = new_cls.data_queue.getInstance()
        self.webdriver_wait = WebDriverWait(self.scraper, 10)

    def set_data(self):
        self.lock.acquire()
        try:
            if not self.data_qu.empty():
                self.data = self.data_qu.get_data()
        except:
            print("data yok")
        self.get_page()

    def get_page(self):
        self.scraper.get(f"https://www.amazon.com/dp/{self.data}?psc=1")
        if webdriver_class.check_target(self.scraper):
            self.get_page_data()
        else:
            webdriver_class.change_target_location(self.scraper)
            self.get_page_data()

    def get_page_data(self):
        json_data = {
            "title": self.get_title(),
            "brand": self.get_brand(),
            "stars": self.get_stars(),
            "stock": self.get_stock(),
            "stock_amount": self.get_stock_amount(),
            "seller": self.get_seller(),
            "sender": self.get_sender(),
            "price": self.get_price(),
            "ratings": self.get_ratings(),
            "target_country": self.check_target_country()
        }
        return self.add_json(json_data)

    def add_json(self, data):
        self.lock.acquire()
        try:
            t_json[f"{self.data}"] = data
        finally:
            print(t_json)
            self.lock.release()

    def get_price(self):
        element = self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "price")))
        price = element.find_element_by_xpath("table/tbody/tr/td[2]/span").text[1::]
        fee = element.find_element_by_xpath("table/tbody/tr/td[2]/span[2]").text.split()[1][1::]
        total_price = float(price) + float(fee)
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
            return False
        return stars.get_attribute('title')

    def check_target_country(self):
        if self.webdriver_wait.until(
                EC.presence_of_element_located((By.ID, "exports_desktop_qualifiedBuybox_tlc_feature_div"))):
            return True
        else:
            return False

    def get_ratings(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "acrCustomerReviewText"))).text

    def get_stock(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "availability"))).text11

    def get_stock_amount(self):
        try:
            select_box = self.scraper.find_element_by_id("quantity")
        except NoSuchElementException:
            return "1"
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        return len(options)

    def get_seller(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "tabular-buybox-truncate-1"))).text

    def get_sender(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "tabular-buybox-truncate-0"))).text

    # def check_twister(self):
    #     try:
    #         self.scraper.find_element_by_id("twister_feature_div")
    #     except NoSuchElementException:
    #         pass
    #     return
