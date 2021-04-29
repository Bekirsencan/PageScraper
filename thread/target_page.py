from selenium.webdriver.support.wait import WebDriverWait

import webdriver as webdriver_class
import target_page_data as target_page_data_class


class targetPage:
    def __init__(self, scraper, data):
        self.data = data
        self.page_data = None
        self.scraper = scraper
        self.webdriver_wait = WebDriverWait(scraper, 10)

    def get_page(self):
        self.scraper.get(f"https://www.amazon.ca/dp/{self.data}")
        webdriver_class.change_postal_code(self.scraper)

    def get_page_data(self):
        self.page_data = target_page_data_class.get_page_data(self.scraper)

    def show_data(self):
        self.get_page()
        self.get_page_data()
        print(self.page_data)
        return self.page_data
