from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def renew_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate("bekir")
        controller.signal(Signal.NEWNYM)


def new_proxy(PROXY_HOST="127.0.0.1", PROXY_PORT=9050):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", PROXY_HOST)
    profile.set_preference("network.proxy.socks_port", PROXY_PORT)
    profile.set_preference("permission.default.stylesheet", 2)
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    options = Options()
    # options.headless = True
    profile.update_preferences()
    return webdriver.Firefox(options=options, firefox_profile=profile,
                             executable_path='/home/bekir/PycharmProjects/Scraper/geckodriver')



