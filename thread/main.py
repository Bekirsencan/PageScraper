import time
import threading
import queue_class as new_class
import consumer_class
import producer_class

cls = new_class.data_queue.getInstance()


def search_data(data2):
    if cls.empty():
        time.sleep(10)
        return search_data(data2)
    else:
        data(data2)


def data(data):
    a = consumer_class.Consumer(data)
    while not cls.empty():
        a.run_consumer()


def produce_data(data2):
    aw = producer_class.Producer(data2)
    aw.get_page(url)


if __name__ == '__main__':
    url = "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A281407%2Cn%3A172532%2Cn%3A3224438011&dc&page=3&qid=1619350666&rnid=172532&ref=sr_pg_3"

    t = threading.Thread(target=search_data, args=(8010,))
    t2 = threading.Thread(target=produce_data, args=(9050,))
    t.start()
    t2.start()
