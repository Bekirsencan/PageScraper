import json
import threading
import proxy
import time
from source_page import sourcePage
from target_page import targetPage
from queue_class import data_queue
from json_file import json_file
import pprint


class Consumer(threading.Thread):
    def __init__(self, PORT, con):
        super().__init__()
        self.lock = threading.Lock()
        self.data_asin = None
        self.event = threading.Event()
        self.thread_con = con
        self.scraper = proxy.new_proxy("127.0.0.1", PORT)
        self.data_queue = data_queue.getInstance()
        self.json_file = json_file.getInstance()

    def wait_for_data(self):
        with self.thread_con:
            self.thread_con.wait()
            self.check_queue()

    def check_queue(self):
        while not self.data_queue.empty():
            self.run_source_consumer()
        self.json_file.show_json_file()
        self.check_list()

    def get_data(self):
        self.lock.acquire()
        try:
            self.data_asin = self.data_queue.get_data()
        finally:
            self.lock.release()

    def get_source_page(self):
        s = sourcePage(self.scraper, self.data_asin)
        if s.get_page():
            json_data = s.get_page_data()
            self.lock.acquire()
            try:
                self.json_file.add_source(self.data_asin, json_data)
            finally:
                self.lock.release()
        else:
            pass

    def run_source_consumer(self):
        self.get_data()
        print(self.data_asin)
        self.get_source_page()

    def get_target_page(self, data):
        t = targetPage(self.scraper, data)
        self.target_json = t.get_page()  ### show data değiştir

    def check_list(self):
        while self.data_queue.list:
            self.lock.acquire()
            try:
                self.data_asin = self.data_queue.list.pop(0)
            finally:
                self.lock.release()
            self.run_target_consumer(self.data_asin)

    def run_target_consumer(self, data):
        print(data)
        self.get_target_page(data)
