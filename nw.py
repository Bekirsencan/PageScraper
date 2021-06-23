import time
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import proxy
import webdriver

# scraper = proxy.new_proxy()
#
# scraper.get("https://www.amazon.ca/EYEFLASHES-Festivals-Halloween-Customized-Animations/dp/B07XNJ198M?ref_=Oct_s9_apbd_omwf_hd_bw_b3dEdEZ&pf_rd_r=PS1M2TJNEK03F7KW5V9C&pf_rd_p=45af352f-5e0c-58ab-8c60-4400f40fcbd9&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=3328163011")
#
# webdriver.change_postal_code(scraper,"K0G 0A0")
#
# time.sleep(10)
# scraper.find_element_by_css_selector(".a-section.olp-link-widget").click()

# def check_fee(fee_text):
#     try:
#         fee = re.search('\$(.*) d',fee_text.lower()).group(1)
#     except :
#         return "0"
#     return fee
string = "1,799.99"
string = string.replace(",",".")
print(string)

# wait = WebDriverWait(scraper, 10)
# wait.until(ec.element_to_be_clickable((By.ID, "aod-pinned-offer-show-more-link"))).click()
# data = scraper.find_element_by_id("aod-pinned-offer")
# price = data.find_element_by_css_selector("span.a-price").text
# price1 = price.replace('\n', ".")
# price2 = float(price1[1::])
# print(f"type : {type(price2)} and price: {price2}")
# aod_elements = scraper.find_elements_by_id("aod-offer")
# for data in aod_elements:
#     price_text = data.find_element_by_css_selector("span.a-price").text
#     price = price_text.replace('\n', ",")
#     print(price)
#     fee_text = data.find_element_by_id("delivery-message").text
#     fee = check_fee(fee_text)
#     print(fee)






#
#
# print(scraper.get_cookies())
#
#
# json_data = { "source":[
#     {
#     "00":{"dasadsd":"adsasd"}},
#     {
#     "aa":{"dasadsd":"adsasd"}
#     }
# ]
# }
# #
# # print(json_data)
# for data in range(len(json_data.get('source'))):
#     if json_data.get('source')[data].get("aa"):
#         del json_data.get('source')[data]
#         break
# print(json_data)
#
# # data = "$0 s"
# # data1 = "10.02"
# # data2 = float(data1) + float(re.search('\$(.*) s', data.lower()).group(1))
# # print(data2)
# proxy