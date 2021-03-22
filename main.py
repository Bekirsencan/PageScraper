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
    "https://www.amazon.com/SunRmex-Protector-Kickstand-Military-Protective/dp/B08VN27HVW/ref=sr_1_1_sspa?dchild=1&qid=1616148011&rnid=2407760011&s=electronics&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExVzVUNzY5SDRPNlM3JmVuY3J5cHRlZElkPUEwMjE2ODk5VzlTS1NVVUlKU0NPJmVuY3J5cHRlZEFkSWQ9QTA0NTAxNjMyRUZYTlY4NFFaS0REJndpZGdldE5hbWU9c3BfYXRmX2Jyb3dzZSZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=")
time.sleep(5)
webdriver.change_target_location(scraper)
time.sleep(5)

var = scraper.find_element_by_css_selector("table.a-normal.a-spacing-micro").find_element_by_xpath("tbody/tr[2]/td[2]")
print(var.text)
