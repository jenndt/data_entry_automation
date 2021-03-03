from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

# Input zillow URL and google form URL:
ZILLOW_URL = ""
FORM_URL = ""

# Input your HTTP Request Header:
header = {
    "User-Agent": "",
    "Accept-Language": ""
}

# Use bs4 to web-scrape the links, addresses, and prices into lists.
response = requests.get(ZILLOW_URL, headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

# Obtain all the links into a list.
all_link_elements = soup.select(".list-card a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    # print(href)
    # Some of the links you get back from Zillow may be incomplete:
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
# print(len(all_links))

# Obtain all the addresses into a list
all_address_elements = soup.select(".list-card-info address")
all_addresses = [address.getText().split(" | ")[-1] for address in all_address_elements]
# print(len(all_addresses))

# Obtain all the prices into a list.
all_price_elements = soup.select(".list-card-heading")
all_prices = []
for element in all_price_elements:
    # Get the prices. However, single & multiple listings have different tag & class structures
    try:
        price = element.select(".list-card-price")[0].contents[0]
    except IndexError:
        # Price with multiple listings
        print("Multiple listings for the card")
        price = element.select(".list-card-details li")[0].contents[0]
    finally:
        all_prices.append(price)
# print(all_prices)

# Create Spreadsheet using Google Form
# Input your path and driver
chrome_driver_path = ""
driver = webdriver.Chrome(executable_path=chrome_driver_path)

for n in range(len(all_links)):
    driver.get(FORM_URL)
    time.sleep(2)
    # In your google form, find the element and link the xpath
    address = driver.find_element_by_xpath('')
    price = driver.find_element_by_xpath('')
    link = driver.find_element_by_xpath('')
    submit_button = driver.find_element_by_xpath('')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
