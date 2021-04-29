import threading
import queue
import proxy, time
import webdriver as webdriver_class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import queue_class as new_cls

a = queue.Queue()
t_json = {}


class Model(threading.Thread):
    def __init__(self, PORT):
        super().__init__()
        self.lock = threading.Lock()
        self.data = None
        self.scraper = proxy.new_proxy("127.0.0.1", PORT)
        self.data_qu = new_cls.data_queue.getInstance()
        self.webdriver_wait = WebDriverWait(self.scraper, 60)

    def new_queue(self):
        if not self.data_qu.empty():
            self.data = self.data_qu.get_data()
            return self.get_page()

    def get_page(self):
        self.scraper.get(f"https://www.amazon.com/dp/{self.data}?psc=1")
        if webdriver_class.check_target(self.scraper):
            return self.get_page_data()
        else:
            webdriver_class.change_target_location(self.scraper)
            return self.get_page_data()

    def get_page_data(self):
        json_data = {
            "title": self.get_title(),
            "brand": self.get_brand(),
            "stars": self.get_stars(),
            "stock": self.get_stock(),
            "stock_amount": self.get_stock_amount(),
            "seller": self.get_seller(),
            "sender": self.get_sender(),
            "price": self.get_saleprice(),
            "ratings": self.get_ratings(),
            "target_country": self.check_target_country()
        }
        return self.add_json(json_data)

    def add_json(self, data):
        print("lock_acquire")
        self.lock.acquire()
        try:
            t_json[f"{self.data}"] = data
        finally:
            print("lock_release")
            print(t_json)
            self.lock.release()
        return self.new_queue()

    def get_ourprice(self):
        try:
            price = self.scraper.find_element_by_id("priceblock_ourprice").text[1::]
            fee = self.scraper.find_element_by_id("ourprice_shippingmessage").text.split()[1][1::]
            total_price = float(price) + float(fee)
        except NoSuchElementException:
            return self.get_saleprice()
        return round(total_price, 2)

    def get_saleprice(self):
        try:
            price = self.scraper.find_element_by_id("priceblock_ourprice").text[1::]
            fee = self.scraper.find_element_by_id("ourprice_shippingmessage").text.split()[1][1::]
            total_price = float(price) + float(fee)
        except NoSuchElementException:
            return self.get_ourprice()
        return round(total_price, 2)

    def get_title(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text
        # return self.scraper.find_element_by_id("productTitle").text

    def get_brand(self):
        var = self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "bylineInfo"))).text.split()
        # var = self.scraper.find_element_by_id('bylineInfo').text.split()
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
            # if self.scraper.find_element_by_id("exports_desktop_qualifiedBuybox_tlc_feature_div"):
            return True
        else:
            return False

    def get_ratings(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "acrCustomerReviewText"))).text
        # return self.scraper.find_element_by_id("acrCustomerReviewText").text

    def get_stock(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "availability"))).text
        # return self.scraper.find_element_by_id("availability").text

    def get_stock_amount(self):
        try:
            select_box = self.scraper.find_element_by_id("quantity")
        except NoSuchElementException:
            return "1"
        options = [x for x in select_box.find_elements_by_tag_name("option")]
        return len(options)

    def get_seller(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "tabular-buybox-truncate-1"))).text
        # return self.scraper.find_element_by_id("tabular-buybox-truncate-1").text

    def get_sender(self):
        return self.webdriver_wait.until(EC.presence_of_element_located((By.ID, "tabular-buybox-truncate-0"))).text
        # return self.scraper.find_element_by_id("tabular-buybox-truncate-0").text


def search_data(data2):
    cls = new_cls.data_queue.getInstance()
    if cls.empty():
        time.sleep(10)
        return search_data(data2)
    else:
        aw = Model(data2)
        aw.new_queue()


def produce_data(data2):
    aw = new_cls.producer_class(data2)
    aw.get_page(url)


# def run_all_thread():
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.map(search_data,list)

if __name__ == '__main__':
    proxy_queue = queue.Queue()
    list = [8010, 9050]
    asin_queue = queue.Queue()
    url = "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A281407%2Cn%3A172532%2Cn%3A3224438011&dc&qid=1617619350&rnid=172532&ref=sr_nr_n_1"

    t = threading.Thread(target=search_data, args=(8010,))
    t2 = threading.Thread(target=produce_data, args=(9050,))
    t.start()
    t2.start()
