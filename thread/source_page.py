from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import webdriver as webdriver_class
import re
import queue_class as new_class


class sourcePage:
    def __init__(self, scraper, data):
        self.data = data
        self.scraper = scraper
        self.webdriver_wait = WebDriverWait(scraper, 10)
        self.data_queue = new_class.data_queue.getInstance()

    def get_page(self):
        self.scraper.get(f"https://www.amazon.com/dp/{self.data}?psc=1")
        if webdriver_class.check_target(self.scraper):
            return self.get_page_data()
        else:
            webdriver_class.change_target_location(self.scraper)
            return self.get_page_data()

    def get_page_data(self):
        self.check_twister()
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
        return json_data

    def get_price(self):
        element = self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "price"))).text
        data = re.split(r'\D+', element)
        if data.__len__() == 6 or data.__len__() == 7:
            total_price = float(data[1]) + float(data[2]) / 100 + float(data[3]) + float(data[4]) / 100
            return round(total_price, 2)
        else:
            total_price = float(data[3]) + float(data[4]) / 100 + float(data[5]) + float(data[6]) / 100
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
        try:
            element = self.scraper.find_element_by_id("acrCustomerReviewText")
        except NoSuchElementException:
            return "yok"
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
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "tabular-buybox-truncate-1"))).text

    def get_sender(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "tabular-buybox-truncate-0"))).text

    def check_twister(self):
        try:
            self.scraper.find_element_by_id("twister_feature_div")
        except NoSuchElementException:
            pass
        self.get_twister_asin()

    def get_twister_asin(self):
        twister_element_list = self.scraper.find_elements_by_xpath("//li[@data-defaultasin]")
        for data in twister_element_list:
            self.data_queue.add_data_to_list(data)

    # def check_queue(self,data):
    #     if not data in self.data_queue:
    #         self.data_queue.add_data(data)
    #     else:
    #         print("var")

