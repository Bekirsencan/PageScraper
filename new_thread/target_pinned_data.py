from selenium.common.exceptions import NoSuchElementException

import get_target_pinned_data


def check_pinned_data(scraper):
    try:
        scraper.find_element_by_css_selector(".a-touch-link.a-box.olp-touch-link").click()
    except NoSuchElementException:
        return False
    return True


def get_pinned_data(scraper):
    json_data = get_target_pinned_data.get_data(scraper)
    return json_data
