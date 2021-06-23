import time
import threading
import queue_class as new_class
import consumer_class
import producer_class

cls = new_class.data_queue.getInstance()


def search_data(data, con):
    a = consumer_class.Consumer(data, con)
    a.wait_for_data()


def data(data, con):
    a = consumer_class.Consumer(data, con)
    a.wait_for_data()


def produce_data(data2, con):
    aw = producer_class.Producer(data2, con)
    aw.get_page(url)


if __name__ == '__main__':
    url = "https://www.amazon.com/s?i=electronics-intl-ship&bbn=16225009011&rh=n%3A281407%2Cn%3A172532%2Cn%3A3224438011&dc&page=9&qid=1620054021&rnid=172532&ref=sr_pg_3"
    condition = threading.Condition()
    t = threading.Thread(target=search_data, args=(8010, condition,))
    t2 = threading.Thread(target=produce_data, args=(9050, condition,))
    t.start()
    t2.start()
