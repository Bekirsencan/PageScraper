# Page Scraper
## Created For Linux.

Amazon page scraper. With this project we can search Amazon products informations such as asin code, title, seller, price vs. and write/read all info's. Used Selenium for the scraping tool.Geckodriver(mozilla) used for the optimal memory usage. Tor used for the IP changes for the blocked IP's. Works with thread so usable with multiple geckodriver instances.

# How To Use
- Download Tor.
- Copy torrc file and create a directory etc/tor/{PortNumber}/tor/ and paste here.
  - For multiple geckodriver instances you can create multiple torrc files.
  - Multiple instances needs different PortNumber and ControlPortNumber.
  - All torrc files must have different PortNumber.
  - ControlPortNumber must be PortNumber + 1 .
- Add port numbers inside mainn.py(line 40-41).
```
open_proxy("8010")
open_proxy("9050")
```
- Create threads for the instances. Thread and instance numbers must be equal.
- Change URL for the product to search.
- Run mainn.py

# Setup

* Create venv
```
py -m venv venv
```
* Activate venv
```
venv\Scripts\activate
```
* Install requirements.txt
```
pip install -r requirements.txt
```

## Libraries and tools 🛠
* [Selenium](https://www.selenium.dev)
* [Stem](https://stem.torproject.org)
* [Tor](https://www.torproject.org)




