import webdriver as webdriver
import proxy
import time

scraper = webdriver.new_proxy("127.0.0.1", 9050)

url = "https://www.amazon.com/s?k=bookshelf&crid=2ZLOCGYEQLDH2&sprefix=bookshe%2Caps%2C363&ref=nb_sb_ss_midas-iss-sm_2_7"
scraper.get(url)
webdriver.change_target_location(scraper)
url_list = []
time.sleep(10)

data = scraper.find_elements_by_xpath("/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div")

/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div[4]/div/span/div/div/div/div/div[2]/h2/a
/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div[4]/div/span/div/div/div/div/div[2]/h2/a
url_list.append(scraper.find_element_by_xpath(url).get_attribute("href"))

# for i in range(0,4):
#
#     url = f"/html/body/div[1]/div[2]/div[1]/div[2]/div/span[3]/div[2]/div[{i}]]/div/span/div/div/div/div/div[2]/h2/a"
#     url_list.append(scraper.find_element_by_xpath(url).get_attribute("href"))

print(url_list)


