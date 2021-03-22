import webdriver as webdriver
import time
import json
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import proxy

scraper = proxy.new_proxy()
proxy.renew_ip()
scraper.get(
    "https://www.amazon.com/CASEKOO-iPhone-12-Pro-Max/dp/B08CXNS295/ref=sr_1_4?dchild=1&qid=1616148011&rnid=2407760011&s=electronics&sr=1-4")
time.sleep(5)
webdriver.change_target_location(scraper)
time.sleep(5)

# scraper.find_element_by_id("olpLinkWidget_feature_div").click()
# time.sleep(2)
# data2 = scraper.find_elements_by_id("aod-offer")


scraper.find_elements_by_id()





# def check():
#     try:
#         scraper.find_element_by_id("productOverview_feature_div")
#     except NoSuchElementException:
#         return False
#     return True
#
# check()
# element = scraper.find_element_by_id("olpLinkWidget_feature_div")
# if ec.visibility_of_element_located((By.CLASS_NAME,"a-section olp-link-widget")):
#     scraper.find_element_by_xpath("//a[@class='a-touch-link a-box olp-touch-link']").click()
#     time.sleep(5)
#     scraper.find_element_by_id("aod-pinned-offer-show-more-link").click()
# else:
#     print("bulunamadı")


# list = []
# list.append("B07RGZ5NKS")
#

# # data = scraper.find_elements_by_id("aod-offer") ### aod offer list
#
#
# element_list = scraper.find_elements_by_xpath("//li[@data-defaultasin]")
#
# for data in element_list:
#     if not data.get_attribute("data-defaultasin") in list:
#         list.append(data.get_attribute("data-defaultasin"))
#
# for data in list:
#     print(data)
