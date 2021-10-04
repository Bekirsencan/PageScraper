import queue_classs

from selenium.common.exceptions import NoSuchElementException

data_queue = queue_classs.data_queue.getInstance()


def check_twister(scraper):
    try:
        scraper.find_element_by_id("twister_feature_div")
    except NoSuchElementException:
        pass
    get_twister_asin(scraper)


def get_twister_asin(scraper):
    twister_element_list = scraper.find_elements_by_css_selector(".swatchAvailable")
    for data in twister_element_list:
        data_queue.add_data_to_list(data.get_attribute("data-defaultasin"))
