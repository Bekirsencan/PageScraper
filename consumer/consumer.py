import proxy as proxy_class
import page as page_class


scraper = None
data_list = []


def main():
    url = f"https://www.amazon.com/dp/{data_list[0]}?psc=1"
    page_class.get_page(scraper, url)


def create_proxy():
    global scraper
    scraper = proxy_class.new_proxy()


def list():
    global data_list
    data_list.append("B08CXNS295")


if __name__ == '__main__':
    list()
    create_proxy()
    main()
