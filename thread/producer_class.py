import threading

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import proxy
import main
import queue_class
import webdriver as webdriver_class
import time
import consumer_class


class Producer:

    def __init__(self, PORT):
        self.element_list = []
        self.lock = threading.Lock()
        self.PORT = PORT
        self.scraper = proxy.new_proxy("127.0.0.1", PORT)
        self.data_qu = queue_class.data_queue.getInstance()

    def get_page(self, url):
        self.scraper.get(url)
        if webdriver_class.check_target(self.scraper):
            self.get_elements()
        else:
            webdriver_class.change_target_location(self.scraper)
            self.get_elements()

    def get_elements(self):
        time.sleep(5)
        self.element_list = WebDriverWait(self.scraper, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@data-asin and @data-uuid]")))
        self.send_producer_list()

    def send_producer_list(self):
        for data in self.element_list:
            self.data_qu.check_queue(data.get_attribute("data-asin"))
        print(len(self.data_qu.queue))
        self.next_page()

    def next_page(self):
        next_button = WebDriverWait(self.scraper, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "a-last")))
        if next_button.get_attribute("class") == "a-last":
            next_button.click()
            self.next_page_data()
        else:
            pass
            # self.scraper.quit()
            # main.data(self.PORT)

    def next_page_data(self):
        webdriver_class.check_target(self.scraper)
        self.get_elements()
