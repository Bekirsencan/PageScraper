import proxy as proxy
import webdriver as webdriver_class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
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
        time.sleep(10)
        self.element_list = WebDriverWait(self.scraper,10).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@data-asin and @data-uuid]")))
        return self.send_producer_list()

    def send_producer_list(self):
        for data in self.element_list:
            if data.get_attribute("data-asin") not in self.producer_list:
                self.producer_list.append(data.get_attribute("data-asin"))

        print(len(self.producer_list))
        return self.next_page()

    def next_page(self):
        next_button = WebDriverWait(self.scraper, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "a-last")))
        if next_button.get_attribute("class") == "a-last":
            next_button.click()
            return self.check_target()
        else:
            for data in self.producer_list:                     ### check next page response for new_proxy()
                print(data)


    def check_target(self): # target country #
        target_country = self.scraper.find_element_by_id("glow-ingress-line2")
        if target_country.text == "Turkey":
            return self.get_elements()
        else:
            webdriver_class.change_target_location(self.scraper)
            return self.get_elements()

