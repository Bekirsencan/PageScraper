from selenium import webdriver
from producer.producer import producer_class
from selenium.common.exceptions import NoSuchElementException
import consumer.page as page_class


def check_twister(page_scraper: webdriver):
    try:
        page_scraper.find_element_by_id("twister_feature_div")
    except NoSuchElementException:
        return page_class.get_page_data(page_scraper)
    return get_twister_asin(page_scraper)


def get_twister_asin(page_scraper: webdriver):
    twister_element_list = page_scraper.find_elements_by_xpath("//li[@data-defaultasin]")
    for data in twister_element_list:
        if not data.get_attribute("data-defaultasin") in producer_class.producer_list:
            producer_class.producer_list.append(data.get_attribute("data-defaultasin"))
        else:
            pass
    return page_class.get_page_data(page_scraper)