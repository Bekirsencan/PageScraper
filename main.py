# from selenium.common.exceptions import NoSuchElementException
import proxy
import consumer.consumer as consumer
import threading
import time


scraper = proxy.new_proxy("127.0.0.1",9050)

def get_data():
    consumer.data("B08J6Q65HY")

def get_data2():
    consumer.data("B08K894JGV")

p = threading.Thread(target=get_data)

p.start()


p.join()

