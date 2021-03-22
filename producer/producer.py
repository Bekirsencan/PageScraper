import proxy as proxy
import webdriver as webdriver_class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class producer_class:
    scraper = None
    element_list = []
    producer_list = []

    def __init__(self):
        self.scraper = proxy.new_proxy()

    def get_page(self, url):
        self.scraper.get(url)
        return self.check_target()

    def get_elements(self):
        self.element_list = self.scraper.find_elements_by_xpath("//div[@data-asin and @data-uuid]")
        return self.send_producer_list()

    def send_producer_list(self):
        for data in self.element_list:
            if data.get_attribute("data-asin") not in self.producer_list:
                self.producer_list.append(data.get_attribute("data-asin"))
        return self.next_page()

    def next_page(self):
        next_button = WebDriverWait(self.scraper, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "a-last")))
        if next_button.get_attribute("class") == "a-last":
            next_button.click()
            return self.check_target()
        else:
            print("işlem bitti") ### check next page response for new_proxy()

    def check_target(self):
        target_country = self.scraper.find_element_by_id("glow-ingress-line2")
        if target_country.text == "Turkey":
            return self.get_elements()
        else:
            webdriver_class.change_target_location(self.scraper)
            return self.get_elements()
