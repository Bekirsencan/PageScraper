import logging
import threading

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import webdriver as webdriver_class
import queue_classs
import time

data_queue = queue_classs.data_queue.getInstance()


def get_page(scraper, url, condition):
    scraper.get(url)  ## sayfa numarasına göre url gitsin # sayfa numara kontrol vs.
    webdriver_class.check_target(scraper)
    run_producer(scraper,condition)


def run_producer(scraper, condition):  ##### Başlangıç sayfa no ve bitiş sayfa no alınsın.
    boolean = True
    while boolean:
        get_elements(scraper)
        boolean = next_page(scraper)
    with condition:
        print("condition notify")
        condition.notify_all()


def get_elements(scraper):
    time.sleep(5)
    element_list = WebDriverWait(scraper, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-asin]")))
    send_producer_list(scraper, element_list)


def send_producer_list(scraper, element_list):
    for data in element_list:
        if not data.get_attribute("data-asin") == "":
            data_queue.check_queue(data.get_attribute("data-asin"))
    print("producer len :")
    print(len(data_queue.queue))


def next_page(scraper):
    next_button = WebDriverWait(scraper, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "a-last")))
    if next_button.get_attribute("class") == "a-last":
        next_button.click()
        return True
    else:
        return False

