import json
import threading
import proxy
import time

import target_consumer
import source_consumer
import queue_classs
import pprint

data_queue = queue_classs.data_queue.getInstance()


def wait_data_source(scraper, condition, lock):
    with condition:
        condition.wait()
        source_consumer.queue_check(scraper,lock)
    target(scraper,lock)


def target(scraper,lock):
    target_consumer.list_check(scraper,lock)
