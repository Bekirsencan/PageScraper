import logging
import threading
import time

import producer
import consumer
import proxy


def run_producer(scraper,condition, lock):  # Url Sayfa Sayısı vs burada alınacak. Alınma konusunda bir class üzerinden singleton ile.
    producer.get_page(scraper, url, condition)


def run_consumer(scraper,condition, lock):
    consumer.wait_data_source(scraper,condition,lock)


def open_proxy(PORT):
    logging.basicConfig(level=logging.INFO)
    logging.info(f'Thread Name= {threading.current_thread().getName()}')
    ### REM2 -> Cookies ekle ilerleyen süreçte URL, Zip Code Cookies üzerinden çek.
    scraper_list.append(proxy.new_proxy("127.0.0.1", PORT))
    logging.info(f'scraper_list = {scraper_list}')


def create_threads():
    condition = threading.Condition()
    lock = threading.Lock()
    thread1 = threading.Thread(target=run_producer, args=(scraper_list.__getitem__(1),condition, lock))
    thread2 = threading.Thread(target=run_consumer, args=(scraper_list.__getitem__(0),condition, lock,))
    thread1.start()
    thread2.start()


### Normal olan burada HTTpRequest olması ardından consumer-producer çalışması
if __name__ == '__main__':
    scraper_list = []
    url = "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A281407%2Cn%3A172532%2Cn%3A3224438011&dc&page=10&qid=1625326208&refresh=1&rnid=172532&ref=sr_pg_10"
    thread_ports = ["9050", "8010"]
    open_proxy("8010")
    open_proxy("9050")
    time.sleep(10)
    create_threads()

