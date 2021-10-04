import target_page_data

import queue_classs
import json_filee

data_queue = queue_classs.data_queue.getInstance()
js = json_filee.json_file.getInstance()


def list_check(scraper, lock):
    while data_queue.list:
        run_consumer(scraper, lock)
    js.show_json_file()


def get_page(scraper, asin):

    return target_page_data.get_page(asin, scraper)


def run_consumer(scraper, lock):
    asin = get_asin(lock)
    json = get_page(scraper, asin)
    lock.acquire()
    try:
            js.add_target(asin, json)
    finally:
        lock.release()


def get_asin(lock):
    lock.acquire()
    try:
        asin = data_queue.list.pop(0)
    finally:
        lock.release()
    return asin
