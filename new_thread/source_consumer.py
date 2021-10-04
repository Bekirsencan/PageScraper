import source_page_data

import queue_classs
import json_filee

data_queue = queue_classs.data_queue.getInstance()
js = json_filee.json_file.getInstance()


def queue_check(scraper, lock):
    while not data_queue.empty():
        run_consumer(scraper, lock)
    js.show_json_file()


def get_page(scraper, asin):
    return source_page_data.get_page(asin, scraper)


def run_consumer(scraper, lock):
    asin = get_asin(lock)
    json = get_page(scraper, asin)
    lock.acquire()
    try:
        if json:
            js.add_source(asin, json)
        else:
            data_queue.delete_from_list(asin)
    finally:
        lock.release()


def get_asin(lock):
    lock.acquire()
    try:
        asin = data_queue.get_data()
    finally:
        lock.release()
    return asin
