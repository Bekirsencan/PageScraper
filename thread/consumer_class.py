import json
import threading
import proxy
import time
from source_page import sourcePage
from target_page import targetPage
from queue_class import data_queue


class Consumer(threading.Thread):
    def __init__(self, PORT):
        super().__init__()
        self.lock = threading.Lock()
        self.data = None
        self.scraper = proxy.new_proxy("127.0.0.1", PORT)
        self.data_queue = data_queue.getInstance()
        self.source_json = None
        self.target_json = None

    def get_data(self):
        self.lock.acquire()
        try:
            self.data = self.data_queue.get_data()
        finally:
            self.lock.release()

    def get_source_page(self):
        s = sourcePage(self.scraper, self.data)
        self.source_json = s.get_page()

    def get_target_page(self):
        t = targetPage(self.scraper, self.data)
        self.target_json = t.show_data()

    def run_consumer(self):
        self.get_data()
        self.get_source_page()
        with open('/home/bekir/Desktop/json.txt', 'a') as file:
            json.dump(self.source_json,file)
            file.write(f"   time = {time.asctime()} \n\n\n")
